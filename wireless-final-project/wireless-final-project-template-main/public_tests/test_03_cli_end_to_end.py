import json
from pathlib import Path

import numpy as np

from conftest import (
    PROJECT_ROOT,
    assert_cli_success,
    call_with_fallback,
    clean_results,
    ensure_test_file,
    find_function,
    read_json,
    read_text,
    run_cli,
)


def test_tc_t_013_sync_detects_25_symbol_offset_if_sync_api_exists():
    synchronize = find_function(
        ["src.synchronization", "src.sync", "src.receiver"],
        ["synchronize", "detect_frame_start", "find_preamble", "sync"],
    )
    rng = np.random.default_rng(2026)
    preamble = np.array([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j] * 8, dtype=complex) / np.sqrt(2)
    payload = np.array([1 - 1j, -1 - 1j, 1 + 1j, -1 + 1j] * 20, dtype=complex) / np.sqrt(2)
    prefix = (rng.normal(size=25) + 1j * rng.normal(size=25)) / np.sqrt(2)
    received = np.concatenate([prefix, preamble, payload])
    try:
        result = call_with_fallback(synchronize, received, preamble=preamble)
    except TypeError:
        result = synchronize(received, preamble)
    if isinstance(result, dict):
        start = result.get("start_index") or result.get("sync_start_index") or result.get("index")
    elif isinstance(result, tuple):
        start = result[0]
    else:
        start = result
    assert abs(int(start) - 25) <= 1


def test_tc_t_014_metrics_json_contains_required_fields(ensure_test_file, clean_results):
    result = run_cli(snr=12, seed=2026)
    assert_cli_success(result)
    metrics_path = PROJECT_ROOT / "results" / "metrics.json"
    assert metrics_path.exists(), "results/metrics.json should be generated"
    metrics = read_json(metrics_path)
    required = {
        "snr_db",
        "seed",
        "modulation",
        "channel",
        "payload_bits",
        "ber",
        "fer",
        "text_match_rate",
        "checksum_pass",
        "sync_start_index",
    }
    missing = sorted(required - set(metrics))
    assert not missing, f"metrics.json missing required fields: {missing}"


def test_tc_t_015_end_to_end_recovers_text_at_12db(ensure_test_file, clean_results):
    result = run_cli(snr=12, seed=2026)
    assert_cli_success(result)
    received_path = PROJECT_ROOT / "results" / "received.txt"
    assert received_path.exists(), "results/received.txt should be generated"
    assert read_text(received_path) == read_text(ensure_test_file)
    metrics = read_json(PROJECT_ROOT / "results" / "metrics.json")
    assert float(metrics["text_match_rate"]) == 1.0


def test_tc_t_016_generates_at_least_two_plot_files(ensure_test_file, clean_results):
    result = run_cli(snr=12, seed=2026)
    assert_cli_success(result)
    expected = [
        PROJECT_ROOT / "results" / "constellation.png",
        PROJECT_ROOT / "results" / "ber_curve.png",
        PROJECT_ROOT / "results" / "sync_peak.png",
    ]
    existing = [path for path in expected if path.exists() and path.stat().st_size > 0]
    assert len(existing) >= 2, (
        "At least two non-empty plot files are required among "
        "constellation.png, ber_curve.png, sync_peak.png"
    )


def test_tc_t_017_unified_cli_runs_without_interactive_input(ensure_test_file, clean_results):
    result = run_cli(snr=12, seed=2026, timeout=20)
    assert_cli_success(result)
    combined_output = (result.stdout + "\n" + result.stderr).lower()
    interactive_hints = ["input(", "请输入", "press enter", "waiting for input"]
    assert not any(hint in combined_output for hint in interactive_hints), (
        "Program should run non-interactively under the unified CLI"
    )


def test_cli_outputs_valid_json_metrics(ensure_test_file, clean_results):
    result = run_cli(snr=12, seed=2026)
    assert_cli_success(result)
    metrics_path = PROJECT_ROOT / "results" / "metrics.json"
    with metrics_path.open("r", encoding="utf-8") as f:
        metrics = json.load(f)
    assert str(metrics["modulation"]).lower() == "qpsk"
    assert str(metrics["channel"]).lower() == "awgn"
    assert int(metrics["seed"]) == 2026
    assert abs(float(metrics["snr_db"]) - 12.0) < 1e-9


def test_main_py_exists_and_uses_argument_parsing():
    main_path = PROJECT_ROOT / "main.py"
    assert main_path.exists(), "main.py is required"
    text = main_path.read_text(encoding="utf-8", errors="ignore").lower()
    assert "--input" in text and "--output" in text, (
        "main.py should support --input and --output command-line arguments"
    )
