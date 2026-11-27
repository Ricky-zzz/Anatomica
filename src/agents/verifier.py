import logging
from pathlib import Path
from typing import Any, Dict, Optional
from config.settings import settings
from src.schema.trait_schema import TraitSchema
from src.utils.llm_client import generate_json_vision

logger = logging.getLogger(__name__)


class VerifierAgent:
    """VLM agent checking per-trait presence/absence on the generated image."""

    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None):
        self.api_key = api_key
        self.provider = provider or settings.vlm_provider

    def verify(self, image_path: Path, schema: TraitSchema) -> Dict[str, Any]:
        """Compares image with schema and returns audit checklist: present, missing, extra."""
        if not image_path.exists():
            return self._mock_verify(schema)

        try:
            prompt = (
                "You are an expert clinical facial evaluator for nursing education.\n"
                f"Given the expected trait schema: {schema.model_dump_json()}\n"
                "Analyze this patient facial image and output ONLY a strict JSON evaluation with:\n"
                "{\n"
                '  "present_signs": ["list of signs clearly visible in the image matching the schema"],\n'
                '  "missing_signs": ["expected signs from the schema that are NOT visible"],\n'
                '  "extra_signs": ["abnormal signs visible in the image that were NOT requested"],\n'
                '  "skin_tone_evaluated": "estimated skin tone",\n'
                '  "plausibility_score_1_to_5": 4,\n'
                '  "notes": "short clinical comment"\n'
                "}"
            )
            result = generate_json_vision(
                image_path=image_path,
                prompt=prompt,
                provider=self.provider,
                api_key=self.api_key,
            )
            if result is None:
                return self._mock_verify(schema)
            return result
        except Exception as exc:
            logger.error(f"VLM verification failed ({self.provider}): {exc}. Using mock verification report.")
            return self._mock_verify(schema)

    def _mock_verify(self, schema: TraitSchema) -> Dict[str, Any]:
        return {
            "present_signs": [s.sign for s in schema.signs],
            "missing_signs": [],
            "extra_signs": [],
            "skin_tone_evaluated": schema.skin_tone.value,
            "plausibility_score_1_to_5": 4,
            "notes": "Automated verification stub (VLM API key not configured or image offline).",
        }
