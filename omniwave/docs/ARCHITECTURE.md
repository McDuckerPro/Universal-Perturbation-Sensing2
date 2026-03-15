# OmniWave Architecture

## Design decisions
- **Sensor-agnostic core**: all sensors emit `SignalFrame`.
- **Adapter pattern**: each sensor implementation subclasses `SensorAdapter`.
- **Universal pipeline**: shared preprocessing/feature extraction/event detection.
- **Fusion first**: multiple processed streams generate confidence + occupancy + motion map.
- **Production-minded plumbing**: recording/replay, firmware protocol, tests, and docs included.

## Runtime flow
1. Adapter emits `SignalFrame`
2. `UniversalSignalPipeline.process` computes filtered signal, FFT, features, events
3. `MotionFieldModel` estimates clusters/trajectory hints
4. `ActivityClassifier` predicts activity labels
5. `MultiSensorFusion` combines streams
6. Dashboard renders live updates
7. `Recorder` optionally persists JSONL for replay
