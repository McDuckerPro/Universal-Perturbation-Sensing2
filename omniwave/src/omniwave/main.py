from __future__ import annotations

import argparse
import sys
from pathlib import Path

from omniwave.adapters import (
    MockLidarAdapter,
    MockUWBAdapter,
    MockWifiCSIAdapter,
    RadarLD2410Adapter,
    RCWL0516RadarAdapter,
    SimulatedAdapter,
    UltrasonicHCSR04Adapter,
)
from omniwave.core.interfaces import SensorAdapter
from omniwave.fusion.multisensor import MultiSensorFusion
from omniwave.models.activity import ActivityClassifier
from omniwave.models.motion import MotionFieldModel
from omniwave.processing.pipeline import UniversalSignalPipeline
from omniwave.storage.recording import Recorder, Replayer


def _build_adapter(mode: str, serial_port: str | None) -> list[SensorAdapter]:
    if mode == "simulated":
        return [SimulatedAdapter(), MockWifiCSIAdapter(), MockUWBAdapter(), MockLidarAdapter()]
    if mode == "serial":
        if serial_port is None:
            raise ValueError("--port required for serial mode")
        return [
            RadarLD2410Adapter(serial_port),
            UltrasonicHCSR04Adapter(serial_port),
            RCWL0516RadarAdapter(serial_port),
        ]
    raise ValueError(f"unsupported mode: {mode}")


def _wire_runtime(dash, adapters: list[SensorAdapter], record_path: Path | None = None) -> None:
    from PySide6.QtCore import QTimer
    pipeline = UniversalSignalPipeline()
    fusion_engine = MultiSensorFusion()
    motion_model = MotionFieldModel()
    classifier = ActivityClassifier()
    recorder = Recorder(record_path) if record_path else None
    streams = [adapter.stream() for adapter in adapters]

    def tick() -> None:
        processed_frames = []
        for stream in streams:
            frame = next(stream)
            if recorder:
                recorder.append(frame)
            processed = pipeline.process(frame)
            motion_model.estimate(processed)
            classifier.predict(processed.features)
            processed_frames.append(processed)
        dash.update_processed(processed_frames[0])
        dash.update_fusion(fusion_engine.fuse(processed_frames))

    timer = QTimer(dash)
    timer.timeout.connect(tick)
    timer.start(120)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="OmniWave universal perturbation sensing platform")
    parser.add_argument("--mode", choices=["simulated", "serial", "replay"], default="simulated")
    parser.add_argument("--port", type=str, help="serial port for hardware mode")
    parser.add_argument("--record", type=Path, help="path to line-delimited JSON recording")
    parser.add_argument("--replay-file", type=Path, help="recording for replay mode")
    args = parser.parse_args(argv)

    if args.mode == "replay":
        if not args.replay_file:
            raise ValueError("--replay-file required in replay mode")
        replay_stream = Replayer(args.replay_file).stream()

        def app_builder(dash) -> None:
            from PySide6.QtCore import QTimer
            pipeline = UniversalSignalPipeline()
            fusion = MultiSensorFusion()

            def tick() -> None:
                frame = next(replay_stream)
                processed = pipeline.process(frame)
                dash.update_processed(processed)
                dash.update_fusion(fusion.fuse([processed]))

            timer = QTimer(dash)
            timer.timeout.connect(tick)
            timer.start(120)

        from omniwave.visualization.dashboard import run_dashboard
        return run_dashboard(app_builder)

    adapters = _build_adapter(args.mode, args.port)
    from omniwave.visualization.dashboard import run_dashboard
    return run_dashboard(lambda dash: _wire_runtime(dash, adapters, record_path=args.record))


def smoke_main() -> int:
    adapter = SimulatedAdapter(seed=21)
    pipeline = UniversalSignalPipeline()
    fusion = MultiSensorFusion()
    stream = adapter.stream()
    processed = [pipeline.process(next(stream)) for _ in range(3)]
    output = fusion.fuse(processed)
    print(
        f"smoke_ok motion_confidence={output.motion_confidence:.3f} occupancy={output.occupancy_estimation:.3f}",
        file=sys.stdout,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
