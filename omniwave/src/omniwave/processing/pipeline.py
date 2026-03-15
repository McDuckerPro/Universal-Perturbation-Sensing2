from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.signal import butter, lfilter

from omniwave.core.signal_frame import ProcessedFrame, SignalFrame


@dataclass
class ProcessingConfig:
    baseline_alpha: float = 0.96
    noise_cutoff_hz: float = 4.0
    event_energy_threshold: float = 0.2
    event_motion_threshold: float = 0.15


@dataclass
class UniversalSignalPipeline:
    config: ProcessingConfig = field(default_factory=ProcessingConfig)
    _baseline: np.ndarray | None = None
    _previous: np.ndarray | None = None

    def preprocess(self, frame: SignalFrame) -> np.ndarray:
        data = frame.data.astype(float)
        data = (data - np.mean(data, axis=1, keepdims=True)) / (np.std(data, axis=1, keepdims=True) + 1e-6)
        nyquist = frame.sample_rate / 2.0
        cutoff_norm = min(self.config.noise_cutoff_hz / max(nyquist, 1e-6), 0.99)
        b, a = butter(2, cutoff_norm, btype="low")
        return lfilter(b, a, data, axis=1)

    def baseline_subtract(self, data: np.ndarray) -> np.ndarray:
        if self._baseline is None:
            self._baseline = data.copy()
        self._baseline = self.config.baseline_alpha * self._baseline + (1 - self.config.baseline_alpha) * data
        return data - self._baseline

    def temporal_derivative(self, data: np.ndarray) -> np.ndarray:
        if self._previous is None:
            self._previous = data.copy()
            return np.zeros_like(data)
        derivative = data - self._previous
        self._previous = data.copy()
        return derivative

    def spectral_analysis(self, data: np.ndarray) -> np.ndarray:
        return np.abs(np.fft.rfft(data, axis=1))

    def extract_features(self, data: np.ndarray, derivative: np.ndarray, spectral: np.ndarray, sample_rate: float) -> dict[str, float]:
        flattened = data.flatten()
        freqs = np.fft.rfftfreq(data.shape[1], d=1.0 / sample_rate)
        spectral_sum = np.sum(spectral) + 1e-9
        dom_idx = int(np.argmax(np.mean(spectral, axis=0)))

        feature_map = {
            "energy": float(np.mean(flattened ** 2)),
            "variance": float(np.var(flattened)),
            "rms": float(np.sqrt(np.mean(flattened ** 2))),
            "peak_to_peak": float(np.ptp(flattened)),
            "temporal_gradient": float(np.mean(np.abs(derivative))),
            "spectral_centroid": float(np.sum(freqs * np.mean(spectral, axis=0)) / spectral_sum),
            "dominant_frequency": float(freqs[dom_idx]),
            "band_energy": float(np.sum(spectral[:, 1:8]) / spectral_sum),
            "cross_channel_correlation": float(self._cross_channel_corr(data)),
            "spatial_coherence": float(np.mean(np.abs(np.fft.fft(data, axis=0)))),
        }
        return feature_map

    @staticmethod
    def _cross_channel_corr(data: np.ndarray) -> float:
        if data.shape[0] == 1:
            return 1.0
        corr = np.corrcoef(data)
        upper = corr[np.triu_indices_from(corr, k=1)]
        return float(np.nanmean(upper))

    def event_detection(self, features: dict[str, float]) -> dict[str, bool]:
        return {
            "motion_event": features["energy"] > self.config.event_energy_threshold,
            "presence": features["temporal_gradient"] > self.config.event_motion_threshold,
            "micromotion": features["dominant_frequency"] < 1.2 and features["rms"] > 0.08,
        }

    def process(self, frame: SignalFrame) -> ProcessedFrame:
        pre = self.preprocess(frame)
        centered = self.baseline_subtract(pre)
        deriv = self.temporal_derivative(centered)
        spectral = self.spectral_analysis(centered)
        features = self.extract_features(centered, deriv, spectral, frame.sample_rate)
        event_flags = self.event_detection(features)
        direction = np.array([features["temporal_gradient"], features["dominant_frequency"], features["spatial_coherence"]])
        return ProcessedFrame(
            frame=frame,
            features=features,
            event_flags=event_flags,
            spectral=spectral,
            motion_intensity=features["energy"],
            motion_direction=direction,
        )
