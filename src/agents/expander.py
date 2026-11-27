import logging
from typing import List, Optional
from config.settings import settings
from src.schema.trait_schema import ClinicalSign, Severity
from src.utils.llm_client import generate_json_text

logger = logging.getLogger(__name__)


class ExpanderAgent:
    """Proposes visible facial signs from disease/condition names (instructor-in-the-loop)."""

    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None):
        self.api_key = api_key
        self.provider = provider or settings.llm_provider

    def expand(self, disease_term: str) -> List[ClinicalSign]:
        """Returns proposed clinical signs that typically manifest visibly on the face."""
        try:
            prompt = (
                f"Given the clinical diagnosis or condition '{disease_term}', propose ONLY the typical VISIBLE signs "
                "that appear on a patient's face. "
                "Output ONLY a valid JSON list of objects with keys: "
                "'sign', 'severity' (mild/moderate/severe), 'region', 'laterality' (optional)."
            )
            items = generate_json_text(
                prompt=prompt,
                provider=self.provider,
                api_key=self.api_key,
            )
            if items is None:
                return self._heuristic_expand(disease_term)
            return [ClinicalSign(**item) for item in items]
        except Exception as exc:
            logger.error(f"LLM expand failed ({self.provider}): {exc}. Using fallback expansion.")
            return self._heuristic_expand(disease_term)

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
