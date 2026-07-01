# Public pytest tests for the wireless final project

These tests are used by the teacher repository's Pull Request grading workflow.
Students should run them locally before creating a Pull Request.

Recommended student project root:

```text
wireless-final-project/
  DESIGN.md
  TEST_PLAN.md
  MOCK_TEST_REPORT.md
  AI_LOG.md
  Test.txt
  main.py
  src/
  tests/
  public_tests/
```

Run locally:

```bash
pip install pytest numpy scipy matplotlib
pytest public_tests -q
```

Required command-line interface:

```bash
python main.py --input Test.txt --output results/received.txt --snr 12 --seed 2026 --mod qpsk --channel awgn
```

The tests use function discovery for module-level checks. Students are encouraged to expose functions using these common names:

| Module | Suggested functions |
|---|---|
| `src/source.py` | `source_encode`, `source_decode`, `text_to_bits`, `bits_to_text` |
| `src/framing.py` | `build_frame`, `parse_frame` |
| `src/crypto.py` or `src/scramble.py` | `scramble`, `descramble`, `encrypt`, `decrypt` |
| `src/channel_coding.py` | `channel_encode`, `channel_decode` |
| `src/modulation.py` | `qpsk_modulate`, `qpsk_demodulate` |
| `src/channel.py` | `awgn`, `awgn_channel`, `add_awgn` |
| `src/synchronization.py` | `synchronize`, `detect_frame_start`, `find_preamble` |

The teacher repository includes a GitHub Actions workflow that runs these tests
when a student opens or updates a Pull Request.

Minimal GitHub Actions workflow:

```yaml
name: PR public grading

on:
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  public-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest numpy scipy matplotlib
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      - name: Run public tests
        run: |
          pytest public_tests -q
```
