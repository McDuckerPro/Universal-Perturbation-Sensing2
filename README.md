# OmniWave — Universal Wave Sensing Platform (MVP)

OmniWave is a production-minded, sensor-agnostic perturbation sensing platform that unifies signal ingestion, processing, fusion, activity understanding, visualization, and hardware integration.

Repository root contains the project in `omniwave/`.

## 1) Architecture proposal (implemented)

### Core principles
- **Universal data container:** `SignalFrame` is the common contract for all sensors.
- **Adapter architecture:** each sensor implementation emits `SignalFrame` through a shared `SensorAdapter` interface.
- **Universal pipeline:** one processing chain for preprocessing, normalization, baseline subtraction, temporal/spectral features, and event detection.
- **Composable models:** motion field estimation, presence/micro-motion rules, and activity classifier.
- **Multi-sensor fusion:** confidence, occupancy, and spatial motion map generated from heterogeneous streams.
- **Operational workflows:** real-time dashboard, recording/replay, firmware protocol, test suite, and deployment docs.

### Project tree
```text
omniwave/
  configs/
  data/
  docs/
  firmware/
  hardware/
  src/omniwave/
    core/
    adapters/
    processing/
    models/
    fusion/
    visualization/
    storage/
    utils/
  tests/
```

### Key design decisions
- Python package managed by `pyproject.toml` with CLI entry points (`omniwave`, `omniwave-smoke`).
- Dashboard implemented with **PySide6 + pyqtgraph** for real-time plots/heatmaps/status panels.
- Serial protocol uses newline-delimited JSON to simplify firmware ↔ host interoperability.
- MVP sensor support includes real adapters (serial-family) and mock/simulated adapters.

### Dependencies
- `numpy`, `scipy`
- `PySide6`, `pyqtgraph`
- `pyserial`, `pydantic`, `pyyaml`
- `scikit-learn`
- dev: `pytest`, `ruff`

## 2) Implementation status

### Implemented modules
- Universal signal container: `SignalFrame`
- Sensor adapters:
  - `SimulatedAdapter`
  - `SerialAdapter`
  - `RadarLD2410Adapter`
  - `UltrasonicHCSR04Adapter`
  - `RCWL0516RadarAdapter`
  - `MockWifiCSIAdapter`
  - `MockUWBAdapter`
  - `MockLidarAdapter`
- Signal pipeline:
  - preprocessing
  - noise filtering
  - normalization
  - baseline subtraction
  - temporal derivative
  - spectral analysis
  - feature extraction
  - event detection
- Motion analysis:
  - motion intensity
  - motion direction hints
  - motion clusters
  - trajectory hint estimation
  - presence and micro-motion rules
- Activity classification: incremental SGD classifier wrapper
- Multi-sensor fusion:
  - motion confidence
  - spatial motion map
  - occupancy estimation
- Storage:
  - JSONL recorder
  - replay stream
- Visualization dashboard:
  - live signal plot
  - FFT plot
  - motion intensity map
  - sensor topology view
  - event panel
  - sensor status
  - 3D scene placeholder (experimental hook)
- ESP32 firmware stub with JSON line output
- Hardware docs, BOM, wiring, flashing instructions
- Unit tests + smoke test

## 3) Quick start

```bash
cd omniwave
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
pytest
omniwave-smoke
omniwave --mode simulated
```

## 4) Modes
- Simulated mode: `omniwave --mode simulated`
- Serial mode: `omniwave --mode serial --port COM5 --record data/recordings/session.jsonl`
- Replay mode: `omniwave --mode replay --replay-file tests/data/sample_replay.jsonl`

## 5) Documentation index
- Architecture: `omniwave/docs/ARCHITECTURE.md`
- Install guide: `omniwave/docs/INSTALL.md`
- Hardware guide: `omniwave/docs/HARDWARE.md`
- Wiring reference: `omniwave/hardware/WIRING.md`
- Firmware source: `omniwave/firmware/esp32/src/main.cpp`
