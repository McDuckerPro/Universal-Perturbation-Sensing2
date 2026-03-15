from __future__ import annotations

from collections import deque

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QWidget

from omniwave.core.signal_frame import ProcessedFrame
from omniwave.fusion.multisensor import FusionOutput


class OmniWaveDashboard(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("OmniWave Dashboard")
        self.resize(1400, 850)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QGridLayout(central)

        self.signal_plot = pg.PlotWidget(title="Live Signal")
        self.fft_plot = pg.PlotWidget(title="FFT Spectrum")
        self.heatmap = pg.ImageView(view=pg.PlotItem(title="Motion Intensity Map"))
        self.topology = pg.PlotWidget(title="Sensor Topology View")
        self.motion_3d_placeholder = QLabel("3D Scene (experimental): enabled via point cloud backend")
        self.event_label = QLabel("Events: none")
        self.status_label = QLabel("Sensors: waiting")

        layout.addWidget(self.signal_plot, 0, 0)
        layout.addWidget(self.fft_plot, 0, 1)
        layout.addWidget(self.heatmap, 1, 0)
        layout.addWidget(self.topology, 1, 1)
        layout.addWidget(self.motion_3d_placeholder, 2, 0)
        layout.addWidget(self.event_label, 2, 1)
        layout.addWidget(self.status_label, 3, 0, 1, 2)

        self._history = deque(maxlen=200)
        self._line = self.signal_plot.plot(pen="c")
        self._fft_line = self.fft_plot.plot(pen="m")

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: None)

    def update_processed(self, frame: ProcessedFrame) -> None:
        mean_signal = np.mean(frame.frame.data, axis=0)
        self._history.extend(mean_signal.tolist())
        self._line.setData(list(self._history))
        self._fft_line.setData(np.mean(frame.spectral, axis=0))
        event_text = ", ".join([k for k, v in frame.event_flags.items() if v]) or "none"
        self.event_label.setText(f"Events: {event_text}")
        self.status_label.setText(f"Sensor: {frame.frame.sensor_type} | Motion={frame.motion_intensity:.3f}")

    def update_fusion(self, fusion: FusionOutput) -> None:
        self.heatmap.setImage(fusion.spatial_motion_map)
        self.topology.clear()
        self.topology.plot(np.linspace(0, 1, fusion.spatial_motion_map.size), fusion.spatial_motion_map.flatten(), pen="y")


def run_dashboard(app_builder) -> int:
    app = QApplication.instance() or QApplication([])
    dash = OmniWaveDashboard()
    dash.show()
    app_builder(dash)
    return app.exec()
