# Installation and Runbook

## Windows setup
1. Install Python 3.10+.
2. Create venv:
   ```powershell
   py -3.10 -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install package:
   ```powershell
   pip install -e .[dev]
   ```

## Run dashboard (simulated multi-sensor)
```bash
omniwave --mode simulated
```

## Run serial mode
```bash
omniwave --mode serial --port COM5 --record data/recordings/session.jsonl
```

## Replay mode
```bash
omniwave --mode replay --replay-file data/recordings/session.jsonl
```

## Smoke test
```bash
omniwave-smoke
pytest
```
