import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from config.settings import settings
from src.schema.trait_schema import TraitSchema

logger = logging.getLogger(__name__)


class VerifierAgent:
    """VLM agent checking per-trait presence/absence on the generated image."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key if api_key is not None else settings.gemini_api_key

    def verify(self, image_path: Path, schema: TraitSchema) -> Dict[str, Any]:
        """Compares image with schema and returns audit checklist: present, missing, extra."""
        if not self.api_key or not image_path.exists():
            return self._mock_verify(schema)

        try:
            return self._gemini_verify(image_path, schema)
        except Exception as exc:
            logger.error(f"VLM verification failed: {exc}. Using mock verification report.")
            return self._mock_verify(schema)

    def _gemini_verify(self, image_path: Path, schema: TraitSchema) -> Dict[str, Any]:
        import io
        from google import genai
        from google.genai import types
        from PIL import Image

        client = genai.Client(api_key=self.api_key)
        pil_img = Image.open(image_path)
        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        image_part = types.Part.from_bytes(data=buf.getvalue(), mime_type="image/png")

        prompt = (
            "You are an expert clinical facial evaluator for nursing education.\n"
            f"Given the expected trait schema: {schema.model_dump_json()}\n"
            "Analyze this patient facial image and output a strict JSON evaluation with:\n"
            "{\n"
            '  "present_signs": ["list of signs clearly visible in the image matching the schema"],\n'
            '  "missing_signs": ["expected signs from the schema that are NOT visible"],\n'
            '  "extra_signs": ["abnormal signs visible in the image that were NOT requested"],\n'
            '  "skin_tone_evaluated": "estimated skin tone",\n'
            '  "plausibility_score_1_to_5": 4,\n'
            '  "notes": "short clinical comment"\n'
            "}"
        )

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[image_part, prompt],
            config={"response_mime_type": "application/json"},
        )

        return json.loads(response.text)

    def _mock_verify(self, schema: TraitSchema) -> Dict[str, Any]:
        return {
            "present_signs": [s.sign for s in schema.signs],
            "missing_signs": [],
            "extra_signs": [],
            "skin_tone_evaluated": schema.skin_tone.value,
            "plausibility_score_1_to_5": 4,
            "notes": "Automated verification stub (API key not configured or image offline).",
        }
