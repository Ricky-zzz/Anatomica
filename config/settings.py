from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


def is_configured_secret(value: str) -> bool:
    """Return True if a secret/key is non-empty and not an example placeholder."""
    cleaned = (value or "").strip()
    if not cleaned:
        return False
    lowered = cleaned.lower()
    return not (lowered.startswith("your_") or lowered.endswith("_here"))


class Settings(BaseSettings):
    # Provider selection
    llm_provider: str = Field(default="opencode", validation_alias="LLM_PROVIDER")
    vlm_provider: str = Field(default="gemini", validation_alias="VLM_PROVIDER")
    image_provider: str = Field(default="cloudflare", validation_alias="IMAGE_PROVIDER")

    # OpenCode Go (OpenAI-compatible endpoint for Parser / Expander / optional VLM)
    opencode_api_key: str = Field(default="", validation_alias="OPENCODE_API_KEY")
    opencode_base_url: str = Field(
        default="https://opencode.ai/zen/go/v1",
        validation_alias="OPENCODE_BASE_URL",
    )
    opencode_model: str = Field(default="deepseek-chat", validation_alias="OPENCODE_MODEL")
    opencode_vision_model: str = Field(default="", validation_alias="OPENCODE_VISION_MODEL")

    # Google AI Studio Free Tier (recommended for VLM Verifier; optional for text)
    gemini_api_key: str = Field(default="", validation_alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.5-flash", validation_alias="GEMINI_MODEL")

    # Cloudflare Workers AI Free Tier (Arm 1 Diffusion: FLUX.1 Schnell / SDXL)
    cloudflare_account_id: str = Field(default="", validation_alias="CLOUDFLARE_ACCOUNT_ID")
    cloudflare_api_token: str = Field(default="", validation_alias="CLOUDFLARE_API_TOKEN")
    cloudflare_image_model: str = Field(
        default="@cf/black-forest-labs/flux-1-schnell",
        validation_alias="CLOUDFLARE_IMAGE_MODEL",
    )

    # 3D Asset Configuration (Arm 2)
    flame_model_path: Path = BASE_DIR / "assets" / "flame" / "flame2023.pkl"
    default_skin_tone: str = Field(default="monk_4", validation_alias="DEFAULT_SKIN_TONE")
    max_edit_loops: int = Field(default=2, validation_alias="MAX_EDIT_LOOPS")

    results_dir: Path = BASE_DIR / "results"
    arm1_dir: Path = BASE_DIR / "results" / "arm1"
    arm2_dir: Path = BASE_DIR / "results" / "arm2"
    assets_dir: Path = BASE_DIR / "assets"
    signs_catalog_path: Path = BASE_DIR / "config" / "signs.json"

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
