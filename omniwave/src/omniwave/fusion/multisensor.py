from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from omniwave.core.signal_frame import ProcessedFrame


@dataclass
class FusionOutput:
    motion_confidence: float
    spatial_motion_map: np.ndarray
    occupancy_estimation: float


class MultiSensorFusion:
    def fuse(self, frames: list[ProcessedFrame]) -> FusionOutput:
        if not frames:
            return FusionOutput(motion_confidence=0.0, spatial_motion_map=np.zeros((8, 8)), occupancy_estimation=0.0)

        confidence = float(np.clip(np.mean([f.features["energy"] for f in frames]) * 4.0, 0.0, 1.0))
        max_bins = max(f.frame.bins for f in frames)
        map_rows = []
        for frame in frames:
            row = np.mean(np.abs(frame.frame.data), axis=0)
            if len(row) < max_bins:
                row = np.pad(row, (0, max_bins - len(row)))
            map_rows.append(row)
        matrix = np.vstack(map_rows)
        reduced = matrix[:, :64] if matrix.shape[1] >= 64 else np.pad(matrix, ((0, 0), (0, 64 - matrix.shape[1])))
        spatial_motion_map = reduced.reshape(reduced.shape[0], 8, 8).mean(axis=0)
        occupancy = float(np.clip(np.count_nonzero(spatial_motion_map > spatial_motion_map.mean()) / spatial_motion_map.size, 0, 1))
        return FusionOutput(motion_confidence=confidence, spatial_motion_map=spatial_motion_map, occupancy_estimation=occupancy)
