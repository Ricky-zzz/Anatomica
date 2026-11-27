from datetime import datetime
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from config.settings import settings
from src.agents.expander import ExpanderAgent
from src.agents.parser import ParserAgent
from src.agents.verifier import VerifierAgent
from src.renderers.diffusion import DiffusionRenderer
from src.renderers.parametric import ParametricRenderer
from src.schema.trait_schema import TraitSchema
from src.utils.audit import save_audit_log
from src.utils.naming import generate_result_filename

logger = logging.getLogger(__name__)


class GenerationPipeline:
    """The fixed comparative pipeline: parse -> expand -> render -> verify -> audit."""

    def __init__(self, api_key: Optional[str] = None, offline: bool = False):
        llm_provider = "offline" if offline else settings.llm_provider
        vlm_provider = "offline" if offline else settings.vlm_provider
        image_provider = "offline" if offline else settings.image_provider

        self.parser = ParserAgent(api_key=api_key, provider=llm_provider)
        self.expander = ExpanderAgent(api_key=api_key, provider=llm_provider)
        self.verifier = VerifierAgent(api_key=api_key, provider=vlm_provider)
        self.diffusion_renderer = DiffusionRenderer(provider=image_provider)
        self.parametric_renderer = ParametricRenderer()

    def parse_input(self, text: str) -> TraitSchema:
        """Step 1: Parse natural text to clinical trait schema."""
        return self.parser.parse(text)

    def expand_disease(self, schema: TraitSchema, disease_name: str) -> TraitSchema:
        """Optional Step: Propose signs for disease-only inputs (with faculty confirmation)."""
        proposed = self.expander.expand(disease_name)
        # Return a new copy — never mutate the original schema in-place
        return schema.model_copy(
            update={"signs": schema.signs + proposed, "source": "disease_expanded"}
        )

    def execute_arm(self, schema: TraitSchema, arm_choice: int) -> Dict[str, Any]:
        """
        Runs generation through selected arm:
          0 -> Arm 1: Diffusion PNG
          1 -> Arm 2: Parametric 3D Head
        """
        if arm_choice == 0:
            target_dir = settings.arm1_dir
            renderer = self.diffusion_renderer
            arm_name = "arm1_diffusion"
        elif arm_choice == 1:
            target_dir = settings.arm2_dir
            renderer = self.parametric_renderer
            arm_name = "arm2_parametric"
        else:
            raise ValueError(f"Invalid arm choice '{arm_choice}'. Choose 0 (Arm 1) or 1 (Arm 2).")

        raw_text = schema.raw_input or "patient"
        base_name = generate_result_filename(raw_text, ext="png")
        image_path = target_dir / base_name
        json_path = target_dir / base_name.replace(".png", ".json")

        # Step 2: Render
        render_result = renderer.render(schema, image_path)

        # Step 3: Verify (VLM per-trait evaluation checklist)
        verification_report = self.verifier.verify(image_path, schema)

        # Step 4: Audit trail compilation
        audit_payload = {
            "timestamp": datetime.now().isoformat(),
            "arm": arm_name,
            "input_text": schema.raw_input,
            "schema": schema.model_dump(),
            "render_metadata": render_result.metadata,
            "latency_ms": render_result.generation_time_ms,
            "verification": verification_report,
            "image_file": str(image_path.name),
            "status": "success" if render_result.error is None else "error",
            "error": render_result.error,
        }

        save_audit_log(json_path, audit_payload)

        return {
            "arm": arm_name,
            "image_path": image_path,
            "json_path": json_path,
            "latency_ms": render_result.generation_time_ms,
            "verification": verification_report,
        }
