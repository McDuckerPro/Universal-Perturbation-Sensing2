from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import datetime
from typing import Any

import numpy as np

from omniwave.core.interfaces import SensorAdapter
from omniwave.core.signal_frame import SignalFrame

try:
    import serial
except ImportError:  # pragma: no cover
    serial = None


class SerialAdapter(SensorAdapter):
    sensor_type = "serial_generic"

    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 0.2) -> None:
        if serial is None:
            raise RuntimeError("pyserial is required for SerialAdapter")
        self._ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

    def _parse_line(self, line: str) -> SignalFrame | None:
        try:
            payload: dict[str, Any] = json.loads(line)
            sensor_type = payload["sensor_type"]
            sample_rate = float(payload.get("sample_rate", 20.0))
            channels = int(payload["channels"])
            bins = int(payload["bins"])
            data = np.array(payload["data"], dtype=float).reshape(channels, bins)
            meta = payload.get("metadata", {})
            frame = SignalFrame(
                timestamp=datetime.utcnow(),
                sensor_type=sensor_type,
                sample_rate=sample_rate,
                channels=channels,
                bins=bins,
                data=data,
                metadata=meta,
            )
            frame.validate()
            return frame
        except (ValueError, KeyError, json.JSONDecodeError):
            return None

    def stream(self) -> Iterator[SignalFrame]:
        while True:
            line = self._ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                continue
            frame = self._parse_line(line)
            if frame is not None:
                yield frame

    def close(self) -> None:
        self._ser.close()


class RadarLD2410Adapter(SerialAdapter):
    sensor_type = "radar_ld2410"


class UltrasonicHCSR04Adapter(SerialAdapter):
    sensor_type = "ultrasonic_hcsr04"


class RCWL0516RadarAdapter(SerialAdapter):
    sensor_type = "radar_rcwl0516"
