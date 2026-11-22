import pytest
from pathlib import Path
from src.pipeline.orchestrator import GenerationPipeline
import config.settings as settings_module


def test_pipeline_offline_execution(tmp_path, monkeypatch):
    # Bug 11 fix: redirect output dirs to tmp_path so tests never pollute results/
    monkeypatch.setattr(settings_module.settings, "arm1_dir", tmp_path / "arm1")
    monkeypatch.setattr(settings_module.settings, "arm2_dir", tmp_path / "arm2")
    (tmp_path / "arm1").mkdir()
    (tmp_path / "arm2").mkdir()

    pipeline = GenerationPipeline(api_key=None)

    # Parse
    schema = pipeline.parse_input("adult male with pale lips and fever flush")
    assert schema.sex.value == "male"

    # Test Arm 0 (Diffusion offline placeholder)
    res_arm0 = pipeline.execute_arm(schema, arm_choice=0)
    assert res_arm0["arm"] == "arm1_diffusion"
    assert Path(res_arm0["image_path"]).exists()
    assert Path(res_arm0["json_path"]).exists()

    # Test Arm 1 (Parametric offline schematic)
    res_arm1 = pipeline.execute_arm(schema, arm_choice=1)
    assert res_arm1["arm"] == "arm2_parametric"
    assert Path(res_arm1["image_path"]).exists()
    assert Path(res_arm1["json_path"]).exists()


def test_expand_disease_does_not_mutate_original(tmp_path, monkeypatch):
    monkeypatch.setattr(settings_module.settings, "arm1_dir", tmp_path / "arm1")
    monkeypatch.setattr(settings_module.settings, "arm2_dir", tmp_path / "arm2")

    pipeline = GenerationPipeline(api_key=None)
    schema = pipeline.parse_input("adult female with pale lips")
    original_sign_count = len(schema.signs)

    expanded = pipeline.expand_disease(schema, "high fever")
    # Original schema should NOT be mutated
    assert len(schema.signs) == original_sign_count
    # Expanded copy should have more signs
    assert len(expanded.signs) > original_sign_count
    assert expanded.source == "disease_expanded"
