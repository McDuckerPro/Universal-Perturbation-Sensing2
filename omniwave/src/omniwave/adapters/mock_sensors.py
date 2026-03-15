from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime

import numpy as np

from omniwave.core.interfaces import SensorAdapter
from omniwave.core.signal_frame import SignalFrame


class _BaseMockAdapter(SensorAdapter):
    sensor_type = "mock"

    def __init__(self, channels: int, bins: int, sample_rate: float, amplitude: float, seed: int = 0) -> None:
        self.channels = channels
        self.bins = bins
        self.sample_rate = sample_rate
        self.amplitude = amplitude
        self.rng = np.random.default_rng(seed)
        self.t = 0

    def stream(self) -> Iterator[SignalFrame]:
        while True:
            wave = np.sin(np.linspace(0, np.pi * 2, self.bins) + self.t / 5) * self.amplitude
            data = np.vstack([wave + self.rng.normal(0, 0.02, self.bins) for _ in range(self.channels)])
            yield SignalFrame(
                timestamp=datetime.utcnow(),
                sensor_type=self.sensor_type,
                sample_rate=self.sample_rate,
                channels=self.channels,
                bins=self.bins,
                data=data,
                metadata={"source": "mock", "tick": self.t},
            )
            self.t += 1

    def close(self) -> None:
        return


class MockWifiCSIAdapter(_BaseMockAdapter):
    sensor_type = "wifi_csi"

    def __init__(self) -> None:
        super().__init__(channels=3, bins=128, sample_rate=30.0, amplitude=0.5, seed=10)


class MockUWBAdapter(_BaseMockAdapter):
    sensor_type = "uwb"

    def __init__(self) -> None:
        super().__init__(channels=4, bins=96, sample_rate=20.0, amplitude=0.65, seed=11)


class MockLidarAdapter(_BaseMockAdapter):
    sensor_type = "lidar"

    def __init__(self) -> None:
        super().__init__(channels=1, bins=180, sample_rate=10.0, amplitude=0.35, seed=12)
