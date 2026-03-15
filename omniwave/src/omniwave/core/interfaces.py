from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator

from omniwave.core.signal_frame import SignalFrame


class SensorAdapter(ABC):
    sensor_type: str

    @abstractmethod
    def stream(self) -> Iterator[SignalFrame]:
        """Yield frames continuously."""

    @abstractmethod
    def close(self) -> None:
        """Release resources."""
