from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import numpy as np


@dataclass(slots=True)
class SignalFrame:
    """Universal sensor sample container used across all processing modules."""

    timestamp: datetime
    sensor_type: str
    sample_rate: float
    channels: int
    bins: int
    data: np.ndarray
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if self.data.shape != (self.channels, self.bins):
            raise ValueError(
                f"SignalFrame data shape mismatch; expected {(self.channels, self.bins)} got {self.data.shape}"
            )
        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be positive")


@dataclass(slots=True)
class ProcessedFrame:
    frame: SignalFrame
    features: dict[str, float]
    event_flags: dict[str, bool]
    spectral: np.ndarray
    motion_intensity: float
    motion_direction: np.ndarray
