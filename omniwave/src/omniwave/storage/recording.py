from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

import numpy as np

from omniwave.core.signal_frame import SignalFrame


class Recorder:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, frame: SignalFrame) -> None:
        payload = {
            "timestamp": frame.timestamp.isoformat(),
            "sensor_type": frame.sensor_type,
            "sample_rate": frame.sample_rate,
            "channels": frame.channels,
            "bins": frame.bins,
            "data": frame.data.tolist(),
            "metadata": frame.metadata,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")


class Replayer:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def stream(self) -> Iterator[SignalFrame]:
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                payload = json.loads(line)
                yield SignalFrame(
                    timestamp=datetime.fromisoformat(payload["timestamp"]),
                    sensor_type=payload["sensor_type"],
                    sample_rate=float(payload["sample_rate"]),
                    channels=int(payload["channels"]),
                    bins=int(payload["bins"]),
                    data=np.array(payload["data"], dtype=float),
                    metadata=payload.get("metadata", {}),
                )
