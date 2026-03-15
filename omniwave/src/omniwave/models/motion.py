from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from omniwave.core.signal_frame import ProcessedFrame


@dataclass
class MotionCluster:
    center_bin: int
    intensity: float
    span: int


@dataclass
class MotionFieldEstimate:
    intensity: float
    direction: np.ndarray
    clusters: list[MotionCluster]
    trajectory_hint: np.ndarray


class MotionFieldModel:
    def estimate(self, processed: ProcessedFrame) -> MotionFieldEstimate:
        signal = np.mean(np.abs(processed.frame.data), axis=0)
        threshold = np.mean(signal) + np.std(signal)
        peaks = np.where(signal > threshold)[0]
        clusters: list[MotionCluster] = []
        if peaks.size:
            groups = np.split(peaks, np.where(np.diff(peaks) > 1)[0] + 1)
            for g in groups:
                clusters.append(MotionCluster(center_bin=int(np.mean(g)), intensity=float(np.max(signal[g])), span=len(g)))
        trajectory_hint = np.array([c.center_bin for c in clusters], dtype=float) if clusters else np.array([], dtype=float)
        return MotionFieldEstimate(
            intensity=processed.motion_intensity,
            direction=processed.motion_direction,
            clusters=clusters,
            trajectory_hint=trajectory_hint,
        )
