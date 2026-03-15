from omniwave.adapters.serial_adapter import SerialAdapter


def test_serial_json_parser_without_io() -> None:
    adapter = object.__new__(SerialAdapter)
    line = '{"sensor_type":"radar_ld2410","sample_rate":10,"channels":1,"bins":3,"data":[[0.1,0.2,0.3]],"metadata":{"id":1}}'
    frame = SerialAdapter._parse_line(adapter, line)
    assert frame is not None
    assert frame.bins == 3
