from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Sex(str, Enum):
    FEMALE = "female"
    MALE = "male"
    OTHER = "other"


class AgeGroup(str, Enum):
    INFANT = "infant"
    CHILD = "child"
    ADOLESCENT = "adolescent"
    ADULT = "adult"
    GERIATRIC = "geriatric"


class MonkSkinTone(str, Enum):
    MONK_01 = "monk_1"
    MONK_02 = "monk_2"
    MONK_03 = "monk_3"
    MONK_04 = "monk_4"
    MONK_05 = "monk_5"
    MONK_06 = "monk_6"
    MONK_07 = "monk_7"
    MONK_08 = "monk_8"
    MONK_09 = "monk_9"
    MONK_10 = "monk_10"


class Severity(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class Laterality(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    BILATERAL = "bilateral"


class ClinicalSign(BaseModel):
    sign: str = Field(description="Normalized identifier of the sign, e.g. jaundice, ptosis")
    severity: Severity = Field(default=Severity.MODERATE, description="Severity grade")
    region: str = Field(description="Facial anatomical region involved, e.g. lips, sclera, eyelid")
    laterality: Optional[Laterality] = Field(
        default=None,
        description="Laterality for asymmetric signs (left, right, bilateral)"
    )


class TraitSchema(BaseModel):
    sex: Sex = Field(default=Sex.FEMALE, description="Biological sex presentation")
    age: AgeGroup = Field(default=AgeGroup.ADULT, description="Apparent age group")
    skin_tone: MonkSkinTone = Field(default=MonkSkinTone.MONK_04, description="Monk Skin Tone Scale (1-10)")
    signs: List[ClinicalSign] = Field(default_factory=list, description="List of present clinical facial signs")
    source: str = Field(default="description", description="Input type: description or disease_expanded")
    raw_input: Optional[str] = Field(default=None, description="Original raw user prompt text")
