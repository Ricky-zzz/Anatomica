import base64
import io
import json
import logging
import time
from pathlib import Path
from typing import Dict, Optional
import httpx
from PIL import Image, ImageDraw
from config.settings import is_configured_secret, settings
from src.renderers.base import BaseRenderer, RenderResult
from src.schema.trait_schema import TraitSchema

logger = logging.getLogger(__name__)


def _load_signs_lookup() -> Dict[str, dict]:
    """Load config/signs.json into a flat {sign_id: entry} dictionary."""
    if not settings.signs_catalog_path.exists():
        return {}
    try:
        catalog = json.loads(settings.signs_catalog_path.read_text(encoding="utf-8"))
        lookup: Dict[str, dict] = {}
        for entries in catalog.get("categories", {}).values():
            for entry in entries:
                if "id" in entry:
                    lookup[entry["id"]] = entry
        return lookup
    except Exception as exc:
        logger.warning(f"Could not load signs catalog: {exc}")
        return {}


class DiffusionRenderer(BaseRenderer):
    """Arm 1: Open-weight Diffusion face generation via Cloudflare Workers AI (FLUX / SDXL)."""

    def __init__(
        self,
        account_id: Optional[str] = None,
        api_token: Optional[str] = None,
        model: Optional[str] = None,
        provider: Optional[str] = None,
    ):
        self.provider = (provider or settings.image_provider or "cloudflare").strip().lower()
        self.account_id = account_id if account_id is not None else settings.cloudflare_account_id
        self.api_token = api_token if api_token is not None else settings.cloudflare_api_token
        self.model = model or settings.cloudflare_image_model
        self._signs_lookup = _load_signs_lookup()

    def render(self, schema: TraitSchema, output_path: Path) -> RenderResult:
        start_time = time.time()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        prompt = self.compile_prompt(schema)
        metadata = {
            "provider": self.provider,
            "model": self.model,
            "prompt": prompt,
            "skin_tone": schema.skin_tone.value,
            "traits": [s.model_dump() for s in schema.signs],
        }

        if (
            self.provider == "offline"
            or not is_configured_secret(self.account_id)
            or not is_configured_secret(self.api_token)
        ):
            logger.info("Cloudflare Workers AI not configured. Generating synthetic Arm 1 placeholder visual.")
            self._generate_placeholder_image(schema, output_path, "ARM 1: DIFFUSION (MOCK)")
            elapsed_ms = (time.time() - start_time) * 1000
            metadata["is_mock"] = True
            return RenderResult(
                arm="arm1_diffusion",
                image_path=output_path,
                metadata=metadata,
                generation_time_ms=elapsed_ms,
            )

        try:
            image_bytes = self._call_cloudflare(prompt)
            image = Image.open(io.BytesIO(image_bytes))
            image.save(output_path, "PNG")

            elapsed_ms = (time.time() - start_time) * 1000
            metadata["is_mock"] = False
            return RenderResult(
                arm="arm1_diffusion",
                image_path=output_path,
                metadata=metadata,
                generation_time_ms=elapsed_ms,
            )
        except Exception as exc:
            logger.error(f"Cloudflare diffusion generation error: {exc}. Generating placeholder fallback.")
            self._generate_placeholder_image(schema, output_path, f"ARM 1 ERROR: {type(exc).__name__}")
            elapsed_ms = (time.time() - start_time) * 1000
            metadata["is_mock"] = True
            return RenderResult(
                arm="arm1_diffusion",
                image_path=output_path,
                metadata=metadata,
                generation_time_ms=elapsed_ms,
                error=str(exc),
            )

    def _call_cloudflare(self, prompt: str, timeout_s: float = 90.0) -> bytes:
        """Invoke Cloudflare Workers AI text-to-image endpoint and return raw image bytes."""
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        payload: dict = {"prompt": prompt}
        if "flux-1-schnell" in self.model:
            payload["num_steps"] = 4

        response = httpx.post(url, json=payload, headers=headers, timeout=timeout_s)
        response.raise_for_status()
        return self._extract_image_bytes(response)

    @staticmethod
    def _extract_image_bytes(response: httpx.Response) -> bytes:
        """Support both FLUX JSON base64 payloads and SDXL raw binary image responses."""
        content_type = response.headers.get("content-type", "").lower()
        if "application/json" in content_type:
            body = response.json()
            b64_data = body.get("result", {}).get("image") or body.get("image")
            if not b64_data:
                raise ValueError(f"Cloudflare JSON response missing image payload: {body}")
            return base64.b64decode(b64_data)
        return response.content

    def compile_prompt(self, schema: TraitSchema) -> str:
        """
        Deterministically compiles a clinical photography prompt from TraitSchema using
        grounded visual phrasing from config/signs.json (zero extra hallucinated signs).
        """
        sign_descriptions = []
        for s in schema.signs:
            entry = self._signs_lookup.get(s.sign, {})
            severity = s.severity.value

            if s.laterality and s.laterality.value in ("left", "right") and entry.get("unilateral_prompt"):
                side = s.laterality.value
                opposite = "right" if side == "left" else "left"
                phrase = entry["unilateral_prompt"].format(side=side, opposite=opposite)
                sign_descriptions.append(f"{severity} {phrase}")
            elif entry.get("visual_prompt"):
                lat_suffix = f" ({s.laterality.value})" if s.laterality else ""
                sign_descriptions.append(f"{severity} {entry['visual_prompt']}{lat_suffix}")
            else:
                lat_str = f"on the {s.laterality.value} side" if s.laterality else ""
                sign_descriptions.append(
                    f"{severity} {s.sign} affecting {s.region} {lat_str}".strip()
                )

        signs_text = "; ".join(sign_descriptions) if sign_descriptions else "no acute distress, normal resting expression"

        prompt = (
            f"Clinical medical education frontal portrait photograph of an {schema.age.value} {schema.sex.value} patient, "
            f"skin tone matching Monk Skin Tone Scale {schema.skin_tone.value}. "
            f"Plain neutral clinic background, even soft clinical lighting, centered head-and-shoulders view looking straight at camera. "
            f"Visible clinical signs: {signs_text}. "
            f"Anatomically accurate medical textbook photography, no extra medical equipment or unrequested symptoms."
        )
        return prompt

    def _generate_placeholder_image(self, schema: TraitSchema, output_path: Path, banner: str):
        """Creates an informative mock PNG for offline testing without burning API tokens."""
        img = Image.new("RGB", (512, 512), color=(235, 240, 248))
        draw = ImageDraw.Draw(img)

        draw.rectangle([10, 10, 502, 60], fill=(30, 64, 175))
        draw.text((25, 28), banner, fill=(255, 255, 255))

        y = 85
        draw.text((25, y), f"Demographics: {schema.age.value} | {schema.sex.value} | {schema.skin_tone.value}", fill=(30, 30, 30))
        y += 35
        draw.text((25, y), "Clinical Signs Rendered:", fill=(30, 30, 30))
        y += 25

        if not schema.signs:
            draw.text((40, y), "- None (Baseline healthy presentation)", fill=(80, 80, 80))
        else:
            for s in schema.signs:
                lat = f" [{s.laterality.value}]" if s.laterality else ""
                draw.text((40, y), f"- {s.sign} ({s.severity.value}, {s.region}){lat}", fill=(180, 20, 20))
                y += 25

        draw.ellipse([176, 230, 336, 430], outline=(100, 100, 120), width=3, fill=(224, 186, 155))
        draw.ellipse([210, 300, 235, 320], fill=(255, 255, 255), outline=(50, 50, 50))
        draw.ellipse([277, 300, 302, 320], fill=(255, 255, 255), outline=(50, 50, 50))
        draw.line([230, 385, 282, 385], fill=(160, 80, 80), width=4)

        draw.text((25, 470), "Offline Placeholder — Set CLOUDFLARE_ACCOUNT_ID & CLOUDFLARE_API_TOKEN in .env", fill=(100, 100, 100))
        img.save(output_path, "PNG")
