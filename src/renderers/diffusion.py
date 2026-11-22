import io
import logging
import time
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw
from config.settings import settings
from src.renderers.base import BaseRenderer, RenderResult
from src.schema.trait_schema import TraitSchema

logger = logging.getLogger(__name__)


class DiffusionRenderer(BaseRenderer):
    """Arm 1: Diffusion-based face generation using Gemini / Imagen API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key if api_key is not None else settings.gemini_api_key

    def render(self, schema: TraitSchema, output_path: Path) -> RenderResult:
        start_time = time.time()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        prompt = self.compile_prompt(schema)
        metadata = {
            "model": settings.gemini_image_model,
            "prompt": prompt,
            "skin_tone": schema.skin_tone.value,
            "traits": [s.model_dump() for s in schema.signs],
        }

        if not self.api_key:
            logger.warning("No GEMINI_API_KEY. Generating synthetic Arm 1 placeholder visual.")
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
            from google import genai

            client = genai.Client(api_key=self.api_key)
            result = client.models.generate_images(
                model=settings.gemini_image_model,
                prompt=prompt,
                config=dict(
                    number_of_images=1,
                    aspect_ratio="1:1",
                    person_generation="ALLOW_ADULT",
                ),
            )

            generated_image = result.generated_images[0]
            image = Image.open(io.BytesIO(generated_image.image.image_bytes))
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
            logger.error(f"Diffusion generation error: {exc}. Generating placeholder fallback.")
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

    def compile_prompt(self, schema: TraitSchema) -> str:
        """Compiles clinical prompt with explicit demographic and clinical injection."""
        sign_descriptions = []
        for s in schema.signs:
            lat_str = f"on the {s.laterality.value} side" if s.laterality else ""
            sign_descriptions.append(
                f"{s.severity.value} {s.sign} affecting {s.region} {lat_str}".strip()
            )

        signs_text = ", ".join(sign_descriptions) if sign_descriptions else "no acute distress"

        prompt = (
            f"Clinical medical education portrait photograph of an {schema.age.value} {schema.sex.value} patient, "
            f"skin tone corresponds to Monk Scale {schema.skin_tone.value}. "
            f"Neutral clinic background, soft clinical lighting, clear frontal facial view. "
            f"Visible clinical manifestations: {signs_text}. "
            f"Accurate anatomical features, educational textbook standard, realistic medical presentation."
        )
        return prompt

    def _generate_placeholder_image(self, schema: TraitSchema, path: Path, title: str) -> None:
        """Creates an informative offline PNG when API key is unavailable."""
        img = Image.new("RGB", (512, 512), color=(28, 36, 48))
        draw = ImageDraw.Draw(img)

        draw.rectangle([(20, 20), (492, 492)], outline=(70, 130, 180), width=3)
        draw.text((40, 50), title, fill=(255, 215, 0))
        draw.text((40, 100), f"Sex: {schema.sex.value}", fill=(220, 220, 220))
        draw.text((40, 130), f"Age: {schema.age.value}", fill=(220, 220, 220))
        draw.text((40, 160), f"Skin Tone: {schema.skin_tone.value}", fill=(220, 220, 220))

        y = 210
        draw.text((40, y), "Clinical Signs:", fill=(100, 200, 255))
        y += 30
        MAX_Y = 420
        for i, s in enumerate(schema.signs):
            if y >= MAX_Y:
                remaining = len(schema.signs) - i
                draw.text((60, y), f"  ... (+{remaining} more signs)", fill=(160, 160, 160))
                break
            lat = f" ({s.laterality.value})" if s.laterality else ""
            draw.text((60, y), f"• {s.sign} - {s.severity.value} [{s.region}]{lat}", fill=(255, 255, 255))
            y += 25

        draw.text((40, 440), "Status: Ready for Gemini API Key", fill=(160, 160, 160))
        img.save(path, "PNG")
