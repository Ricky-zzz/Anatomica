from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from src.schema.trait_schema import TraitSchema


class RenderResult(BaseModel):
    arm: str = Field(description="Arm identifier: arm1_diffusion or arm2_parametric")
    image_path: Path = Field(description="Absolute or relative path to generated PNG image")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Execution metadata, params, seeds, etc.")
    generation_time_ms: float = Field(default=0.0, description="Latency in milliseconds")
    error: Optional[str] = Field(default=None, description="Error message if rendering failed")


class BaseRenderer(ABC):
    """Abstract base class for patient facial renderers."""

    @abstractmethod
    def render(self, schema: TraitSchema, output_path: Path) -> RenderResult:
        """Render patient face based on TraitSchema and save to output_path."""
        pass
