from pathlib import Path

from conftest import PROJECT_ROOT, read_text, text_file_mentions


def test_tc_t_001_required_project_files_exist():
    required = [
        "DESIGN.md",
        "TEST_PLAN.md",
        "MOCK_TEST_REPORT.md",
        "AI_LOG.md",
        "main.py",
        "src",
        "tests",
    ]
    missing = [path for path in required if not (PROJECT_ROOT / path).exists()]
    assert not missing, f"Missing required project paths: {missing}"


def test_tc_t_002_design_covers_fixed_system_chain():
    keywords = [
        "Source Encode",
        "Encrypt",
        "Scramble",
        "Channel Encode",
        "Frame Build",
        "QPSK",
        "Modulate",
        "Demodulate",
        "Channel",
        "Synchronization",
        "Channel Decode",
        "Source Decode",
        "Metrics",
    ]
    hits = text_file_mentions("DESIGN.md", keywords, min_count=9)
    assert "QPSK" in hits, "DESIGN.md must explicitly mention QPSK"


def test_tc_t_003_mock_report_contains_revision_record():
    text = read_text(PROJECT_ROOT / "MOCK_TEST_REPORT.md")
    normalized = text.lower()
    mock_count = normalized.count("mock")
    assert mock_count >= 3, "MOCK_TEST_REPORT.md should describe at least 3 mock tests"
    risk_words = ["风险", "缺陷", "问题", "failure", "risk", "defect", "issue"]
    revision_words = ["修订", "修改", "调整", "revise", "revision", "update", "change"]
    assert any(word in normalized for word in risk_words), (
        "MOCK_TEST_REPORT.md should describe at least one design risk or defect"
    )
    assert any(word in normalized for word in revision_words), (
        "MOCK_TEST_REPORT.md should describe DESIGN.md revisions"
    )


def test_tc_t_018_ai_log_records_ai_assistance():
    text = read_text(PROJECT_ROOT / "AI_LOG.md")
    normalized = text.lower()
    prompt_count = normalized.count("prompt") + normalized.count("提示")
    assert prompt_count >= 3, "AI_LOG.md should record at least 3 prompts or interactions"
    assert any(word in normalized for word in ["人工", "修改", "manual", "edited", "change"]), (
        "AI_LOG.md should explain human modifications to AI-generated content"
    )
    assert any(word in normalized for word in ["采纳", "理由", "reason", "adopt"]), (
        "AI_LOG.md should explain final adoption reasons"
    )


def test_tc_t_019_report_or_design_explains_results():
    candidate_files = [
        PROJECT_ROOT / "REPORT.md",
        PROJECT_ROOT / "ANALYSIS.md",
        PROJECT_ROOT / "DESIGN.md",
        PROJECT_ROOT / "MOCK_TEST_REPORT.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in candidate_files if path.exists())
    normalized = text.lower()
    assert "qpsk" in normalized or "星座" in normalized, (
        "Report or DESIGN.md should explain QPSK constellation results"
    )
    assert "ber" in normalized or "误码" in normalized or "text_match_rate" in normalized, (
        "Report or DESIGN.md should discuss BER or text_match_rate"
    )
    assert any(word in normalized for word in ["失败", "误码", "噪声", "snr", "failure", "error"]), (
        "Report or DESIGN.md should explain at least one failure or error cause"
    )


def test_tc_t_020_no_obvious_direct_file_copy_shortcut():
    source_files = list((PROJECT_ROOT / "src").rglob("*.py")) + [PROJECT_ROOT / "main.py"]
    combined = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in source_files if path.exists())
    suspicious_patterns = [
        "shutil.copy",
        "copyfile",
        "received.txt').write_text(Path('Test.txt')",
        'received.txt").write_text(Path("Test.txt")',
    ]
    found = [pattern for pattern in suspicious_patterns if pattern in combined]
    assert not found, f"Suspicious direct file-copy shortcut found: {found}"
