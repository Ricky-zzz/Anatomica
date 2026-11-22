from src.agents.parser import ParserAgent
from src.schema.trait_schema import AgeGroup, Laterality, Sex


def test_heuristic_parser():
    parser = ParserAgent(api_key="")
    text = "Female elderly patient with runny nose, yellow sclera, and left ptosis"
    schema = parser.parse(text)

    assert schema.sex == Sex.FEMALE
    assert schema.age == AgeGroup.GERIATRIC
    sign_names = [s.sign for s in schema.signs]
    assert "rhinorrhea" in sign_names
    assert "jaundice" in sign_names
    assert "ptosis" in sign_names

    # Check laterality
    ptosis = next(s for s in schema.signs if s.sign == "ptosis")
    assert ptosis.laterality == Laterality.LEFT
