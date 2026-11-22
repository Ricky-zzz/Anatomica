import json
import logging
import re
from typing import Optional
from config.settings import settings
from src.schema.trait_schema import (
    AgeGroup,
    ClinicalSign,
    Laterality,
    MonkSkinTone,
    Severity,
    Sex,
    TraitSchema,
)

logger = logging.getLogger(__name__)


class ParserAgent:
    """Parses free-text clinical description into a structured TraitSchema."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key if api_key is not None else settings.gemini_api_key

    def parse(self, text: str) -> TraitSchema:
        """Parse natural language into TraitSchema."""
        if not self.api_key:
            logger.warning("No GEMINI_API_KEY detected. Using fallback heuristic parser.")
            return self._heuristic_parse(text)

        try:
            return self._gemini_parse(text)
        except Exception as exc:
            logger.error(f"Gemini parse failed: {exc}. Falling back to heuristic parse.")
            return self._heuristic_parse(text)

    def _gemini_parse(self, text: str) -> TraitSchema:
        from google import genai

        client = genai.Client(api_key=self.api_key)
        system_instruction = (
            "You are a clinical facial sign extractor for nursing education. "
            "Extract demographic traits and visible facial signs from the given description. "
            "Output ONLY valid JSON adhering to the following schema:\n"
            "{\n"
            '  "sex": "female" | "male" | "other",\n'
            '  "age": "infant" | "child" | "adolescent" | "adult" | "geriatric",\n'
            '  "skin_tone": "monk_1" to "monk_10",\n'
            '  "signs": [\n'
            '    {"sign": "string", "severity": "mild"|"moderate"|"severe", "region": "string", "laterality": "left"|"right"|"bilateral"|null}\n'
            "  ]\n"
            "}"
        )

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=f"Patient description: {text}",
            config={"system_instruction": system_instruction, "response_mime_type": "application/json"},
        )

        data = json.loads(response.text)
        data["raw_input"] = text
        data["source"] = "description"
        return TraitSchema(**data)

    def _heuristic_parse(self, text: str) -> TraitSchema:
        """Rule-based offline fallback for rapid testing and unit tests."""
        lower = text.lower()

        def has_word(word: str) -> bool:
            return bool(re.search(rf"\b{re.escape(word)}\b", lower))

        sex = Sex.FEMALE if any(has_word(w) for w in ["female", "woman", "girl", "she", "her"]) else Sex.MALE
        age = AgeGroup.ADULT
        if any(has_word(w) for w in ["elderly", "old", "geriatric", "senior"]):
            age = AgeGroup.GERIATRIC
        elif any(has_word(w) for w in ["child", "kid", "boy", "girl", "pediatric"]):
            age = AgeGroup.CHILD

        signs = []
        if has_word("jaundice") or has_word("yellow") or has_word("yellowish"):
            signs.append(ClinicalSign(sign="jaundice", severity=Severity.MODERATE, region="sclera_skin"))
        if has_word("pallor") or has_word("pale"):
            signs.append(ClinicalSign(sign="pallor", severity=Severity.MODERATE, region="lips"))
        if has_word("cyanosis") or has_word("bluish") or has_word("cyanotic"):
            signs.append(ClinicalSign(sign="cyanosis", severity=Severity.MODERATE, region="lips"))
        if has_word("flush") or has_word("flushed") or has_word("erythema"):
            signs.append(ClinicalSign(sign="flushing", severity=Severity.MODERATE, region="cheeks"))
        if has_word("runny") or has_word("rhinorrhea") or has_word("nasal discharge"):
            signs.append(ClinicalSign(sign="rhinorrhea", severity=Severity.MILD, region="nose"))
        if has_word("ptosis") or has_word("drooping eyelid"):
            lat = Laterality.LEFT if has_word("left") else (Laterality.RIGHT if has_word("right") else None)
            signs.append(ClinicalSign(sign="ptosis", severity=Severity.MODERATE, region="eyelid", laterality=lat))
        if has_word("droop") or has_word("facial droop") or has_word("facial asymmetry"):
            lat = Laterality.LEFT if has_word("left") else (Laterality.RIGHT if has_word("right") else None)
            signs.append(ClinicalSign(sign="facial_droop", severity=Severity.MODERATE, region="mouth", laterality=lat))

        return TraitSchema(
            sex=sex,
            age=age,
            skin_tone=MonkSkinTone.MONK_04,
            signs=signs,
            source="description",
            raw_input=text,
        )
