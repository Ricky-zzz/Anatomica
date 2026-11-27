import base64
import httpx
from config.settings import is_configured_secret
from src.renderers.diffusion import DiffusionRenderer
from src.schema.trait_schema import (
    AgeGroup,
    ClinicalSign,
    Laterality,
    MonkSkinTone,
    Severity,
    Sex,
    TraitSchema,
)
from src.utils.llm_client import parse_json_response


def test_is_configured_secret():
    assert not is_configured_secret("")
    assert not is_configured_secret("your_gemini_api_key_here")
    assert not is_configured_secret("YOUR_CLOUDFLARE_TOKEN_HERE")
    assert is_configured_secret("sk-live-real-token-12345")


def test_parse_json_response_strips_markdown_fences():
    fenced = '```json\n{"sex": "female", "signs": []}\n```'
    parsed = parse_json_response(fenced)
    assert parsed == {"sex": "female", "signs": []}


def test_compile_prompt_uses_grounded_clinical_and_unilateral_phrasing():
    renderer = DiffusionRenderer(provider="offline")
    schema = TraitSchema(
        sex=Sex.FEMALE,
        age=AgeGroup.GERIATRIC,
        skin_tone=MonkSkinTone.MONK_05,
        signs=[
            ClinicalSign(sign="jaundice", severity=Severity.MODERATE, region="sclera"),
            ClinicalSign(
                sign="ptosis",
                severity=Severity.SEVERE,
                region="eyelid",
                laterality=Laterality.LEFT,
            ),
        ],
    )
    prompt = renderer.compile_prompt(schema)

    assert "scleral icterus" in prompt
    assert "left upper eyelid" in prompt
    assert "right eye remains normally open" in prompt
    assert "monk_5" in prompt


def test_cloudflare_extract_image_bytes_json_base64():
    raw = b"\x89PNG\r\n\x1a\nfake-png-bytes"
    encoded = base64.b64encode(raw).decode("ascii")
    response = httpx.Response(
        status_code=200,
        headers={"content-type": "application/json"},
        json={"result": {"image": encoded}, "success": True},
    )
    assert DiffusionRenderer._extract_image_bytes(response) == raw


def test_cloudflare_extract_image_bytes_raw_binary():
    raw = b"\x89PNG\r\n\x1a\nraw-sdxl-bytes"
    response = httpx.Response(
        status_code=200,
        headers={"content-type": "image/png"},
        content=raw,
    )
    assert DiffusionRenderer._extract_image_bytes(response) == raw
