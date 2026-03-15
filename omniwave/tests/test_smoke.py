from omniwave.main import smoke_main


def test_smoke_main_runs() -> None:
    assert smoke_main() == 0
