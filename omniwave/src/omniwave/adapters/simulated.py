from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime

import numpy as np

from omniwave.core.interfaces import SensorAdapter
from omniwave.core.signal_frame import SignalFrame


class SimulatedAdapter(SensorAdapter):
    sensor_type = "simulated"

    def __init__(self, sample_rate: float = 20.0, channels: int = 4, bins: int = 64, seed: int = 7) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.bins = bins
        self.rng = np.random.default_rng(seed)
        self._tick = 0

    def stream(self) -> Iterator[SignalFrame]:
        while True:
            base = self.rng.normal(loc=0.0, scale=0.03, size=(self.channels, self.bins))
            moving_peak = int((np.sin(self._tick / 10.0) + 1) * (self.bins - 1) / 2)
            base[:, moving_peak] += 0.8
            data = base + (self.rng.random((self.channels, self.bins)) * 0.05)
            frame = SignalFrame(
                timestamp=datetime.utcnow(),
                sensor_type=self.sensor_type,
                sample_rate=self.sample_rate,
                channels=self.channels,
                bins=self.bins,
                data=data,
                metadata={"tick": self._tick},
            )
            frame.validate()
            self._tick += 1
            yield frame

    def close(self) -> None:
        return
