from datetime import datetime

import numpy as np

from omniwave.core.signal_frame import SignalFrame
from omniwave.processing.pipeline import UniversalSignalPipeline


def test_pipeline_extracts_required_features() -> None:
    frame = SignalFrame(
        timestamp=datetime.utcnow(),
        sensor_type="test",
        sample_rate=20.0,
        channels=2,
        bins=32,
        data=np.random.randn(2, 32),
        metadata={},
    )
    processed = UniversalSignalPipeline().process(frame)
    required = {
        "energy",
        "variance",
        "rms",
        "peak_to_peak",
        "temporal_gradient",
        "spectral_centroid",
        "dominant_frequency",
        "band_energy",
        "cross_channel_correlation",
        "spatial_coherence",
    }
    assert required.issubset(processed.features.keys())
