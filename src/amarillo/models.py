from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import read_json


@dataclass(frozen=True)
class VideoModel:
    id: str
    provider: str
    endpoint: str
    mode: str
    license: str
    default_duration_seconds: int
    estimated_cost_usd: float
    cost_basis: str
    strengths: list[str]
    risks: list[str]
    required_inputs: list[str]
    default_input: dict[str, Any]
    source_url: str


def load_models(catalog_path: Path) -> list[VideoModel]:
    return [VideoModel(**row) for row in read_json(catalog_path)]


def compatible_models(models: list[VideoModel], mode: str | None = None) -> list[VideoModel]:
    if mode is None:
        return models
    return [model for model in models if model.mode == mode or mode in model.mode]
