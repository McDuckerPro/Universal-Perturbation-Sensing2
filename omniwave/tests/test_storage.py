from datetime import datetime

import numpy as np

from omniwave.core.signal_frame import SignalFrame
from omniwave.storage.recording import Recorder, Replayer


def test_record_and_replay_roundtrip(tmp_path) -> None:
    frame = SignalFrame(
        timestamp=datetime.utcnow(),
        sensor_type="simulated",
        sample_rate=10.0,
        channels=1,
        bins=4,
        data=np.array([[1.0, 2.0, 3.0, 4.0]]),
        metadata={"k": "v"},
    )
    path = tmp_path / "capture.jsonl"
    Recorder(path).append(frame)
    replayed = next(Replayer(path).stream())
    assert replayed.sensor_type == frame.sensor_type
    assert replayed.data.shape == frame.data.shape
