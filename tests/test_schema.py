import pytest
from src.schema.trait_schema import (
    AgeGroup,
    ClinicalSign,
    Laterality,
    MonkSkinTone,
    Severity,
    Sex,
    TraitSchema,
)


def test_trait_schema_creation():
    schema = TraitSchema(
        sex=Sex.FEMALE,
        age=AgeGroup.ADULT,
        skin_tone=MonkSkinTone.MONK_03,
        signs=[
            ClinicalSign(
                sign="jaundice",
                severity=Severity.MODERATE,
                region="sclera_skin",
                laterality=None,
            ),
            ClinicalSign(
                sign="ptosis",
                severity=Severity.MILD,
                region="eyelid",
                laterality=Laterality.LEFT,
            ),
        ],
    )

    assert schema.sex == Sex.FEMALE
    assert schema.age == AgeGroup.ADULT
    assert len(schema.signs) == 2
    assert schema.signs[1].laterality == Laterality.LEFT
    assert "jaundice" in [s.sign for s in schema.signs]


def test_schema_serialization():
    sign = ClinicalSign(sign="pallor", severity=Severity.SEVERE, region="lips")
    schema = TraitSchema(signs=[sign])
    serialized = schema.model_dump()

    assert serialized["signs"][0]["sign"] == "pallor"
    assert serialized["signs"][0]["severity"] == "severe"
