from omniwave.adapters import MockLidarAdapter, MockUWBAdapter, MockWifiCSIAdapter, SimulatedAdapter


def test_simulated_adapter_shape() -> None:
    frame = next(SimulatedAdapter(channels=3, bins=16).stream())
    assert frame.data.shape == (3, 16)


def test_mock_adapters_emit_frames() -> None:
    for adapter in [MockWifiCSIAdapter(), MockUWBAdapter(), MockLidarAdapter()]:
        frame = next(adapter.stream())
        assert frame.sensor_type
        assert frame.channels >= 1
