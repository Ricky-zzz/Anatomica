from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    gemini_api_key: str = Field(default="", validation_alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.5-flash", validation_alias="GEMINI_MODEL")
    gemini_image_model: str = Field(default="imagen-3.0-generate-002", validation_alias="GEMINI_IMAGE_MODEL")

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
