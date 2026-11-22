import json
import logging
from typing import List, Optional
from config.settings import settings
from src.schema.trait_schema import ClinicalSign, Severity

logger = logging.getLogger(__name__)


class ExpanderAgent:
    """Proposes visible facial signs from disease/condition names (instructor-in-the-loop)."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key if api_key is not None else settings.gemini_api_key

    def expand(self, disease_term: str) -> List[ClinicalSign]:
        """Returns proposed clinical signs that typically manifest visibly on the face."""
        if not self.api_key:
            return self._heuristic_expand(disease_term)

        try:
            return self._gemini_expand(disease_term)
        except Exception as exc:
            logger.error(f"Gemini expand failed: {exc}. Using fallback expansion.")
            return self._heuristic_expand(disease_term)

    def _gemini_expand(self, disease_term: str) -> List[ClinicalSign]:
        from google import genai

        client = genai.Client(api_key=self.api_key)
        prompt = (
            f"Given the clinical diagnosis or condition '{disease_term}', propose ONLY the typical VISIBLE signs "
            "that appear on a patient's face. "
            "Output a JSON list of objects with keys: 'sign', 'severity' (mild/moderate/severe), 'region', 'laterality' (optional)."
        )

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )

        items = json.loads(response.text)
        return [ClinicalSign(**item) for item in items]

    def _heuristic_expand(self, disease_term: str) -> List[ClinicalSign]:
        lower = disease_term.lower()
        if "fever" in lower:
            return [
                ClinicalSign(sign="flushing", severity=Severity.MODERATE, region="cheeks"),
                ClinicalSign(sign="diaphoresis", severity=Severity.MILD, region="forehead"),
                ClinicalSign(sign="glassy_eyes", severity=Severity.MILD, region="eyes"),
            ]
        if "jaundice" in lower or "hepatitis" in lower or "liver" in lower:
            return [
                ClinicalSign(sign="jaundice", severity=Severity.MODERATE, region="sclera_skin"),
            ]
        if "stroke" in lower or "palsy" in lower:
            return [
                ClinicalSign(sign="facial_droop", severity=Severity.MODERATE, region="mouth"),
            ]
        return [
            ClinicalSign(sign="pallor", severity=Severity.MILD, region="skin"),
        ]
