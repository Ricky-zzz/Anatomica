import base64
import io
import json
import logging
import re
from pathlib import Path
from typing import Any, Optional
import httpx
from config.settings import is_configured_secret, settings

logger = logging.getLogger(__name__)


def parse_json_response(raw_text: str) -> Any:
    """Parse JSON from an LLM response, stripping optional markdown code fences."""
    cleaned = (raw_text or "").strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", cleaned)
    if fence_match:
        cleaned = fence_match.group(1).strip()
    return json.loads(cleaned)


def _get_provider_key(provider: str, override_key: Optional[str] = None) -> str:
    if override_key is not None:
        return override_key
    if provider == "opencode":
        return settings.opencode_api_key
    if provider == "gemini":
        return settings.gemini_api_key
    return ""


def generate_json_text(
    prompt: str,
    system_instruction: Optional[str] = None,
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout_s: float = 45.0,
) -> Optional[Any]:
    """
    Call the configured text LLM provider (OpenCode Go or Gemini AI Studio Free Tier)
    and return parsed JSON. Returns None if offline or no valid key is configured.
    """
    active_provider = (provider or settings.llm_provider or "offline").strip().lower()
    if active_provider == "offline":
        return None

    key = _get_provider_key(active_provider, api_key)
    if not is_configured_secret(key):
        return None

    if active_provider == "opencode":
        url = f"{settings.opencode_base_url.rstrip('/')}/chat/completions"
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": settings.opencode_model,
            "messages": messages,
            "temperature": 0.1,
        }
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        response = httpx.post(url, json=payload, headers=headers, timeout=timeout_s)
        response.raise_for_status()
        body = response.json()
        content = body["choices"][0]["message"]["content"]
        return parse_json_response(content)

    if active_provider == "gemini":
        from google import genai

        client = genai.Client(api_key=key)
        config: dict[str, Any] = {"response_mime_type": "application/json"}
        if system_instruction:
            config["system_instruction"] = system_instruction

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=config,
        )
        return parse_json_response(response.text)

    raise ValueError(f"Unsupported LLM provider: {active_provider}")


def generate_json_vision(
    image_path: Path,
    prompt: str,
    provider: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout_s: float = 60.0,
) -> Optional[Any]:
    """
    Call the configured VLM provider (Gemini AI Studio Free Tier or OpenCode Go vision)
    with a PNG image and return parsed JSON. Returns None if offline or unconfigured.
    """
    active_provider = (provider or settings.vlm_provider or "offline").strip().lower()
    if active_provider == "offline" or not image_path.exists():
        return None

    key = _get_provider_key(active_provider, api_key)
    if not is_configured_secret(key):
        return None

    from PIL import Image

    pil_img = Image.open(image_path)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    if active_provider == "gemini":
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)
        image_part = types.Part.from_bytes(data=png_bytes, mime_type="image/png")
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=[image_part, prompt],
            config={"response_mime_type": "application/json"},
        )
        return parse_json_response(response.text)

    if active_provider == "opencode":
        url = f"{settings.opencode_base_url.rstrip('/')}/chat/completions"
        b64_img = base64.b64encode(png_bytes).decode("ascii")
        model_name = settings.opencode_vision_model or settings.opencode_model
        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{b64_img}"},
                        },
                    ],
                }
            ],
            "temperature": 0.1,
        }
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }
        response = httpx.post(url, json=payload, headers=headers, timeout=timeout_s)
        response.raise_for_status()
        body = response.json()
        content = body["choices"][0]["message"]["content"]
        return parse_json_response(content)

    raise ValueError(f"Unsupported VLM provider: {active_provider}")
