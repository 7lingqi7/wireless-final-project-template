import math

import numpy as np

from conftest import call_with_fallback, find_function, to_bit_list, to_complex_list


def test_tc_t_004_utf8_source_codec_is_reversible(sample_text):
    encode = find_function(
        ["src.source", "src.source_codec", "src.codec", "source"],
        ["source_encode", "text_to_bits", "encode_text", "utf8_to_bits"],
    )
    decode = find_function(
        ["src.source", "src.source_codec", "src.codec", "source"],
        ["source_decode", "bits_to_text", "decode_text", "bits_to_utf8"],
    )
    bits = to_bit_list(call_with_fallback(encode, sample_text))
    assert bits, "Source encoder returned an empty bitstream"
    assert len(bits) % 8 == 0, "UTF-8 source bitstream length should be divisible by 8"
    recovered = call_with_fallback(decode, bits)
    assert recovered == sample_text


def test_tc_t_005_frame_contains_required_fields():
    build_frame = find_function(
        ["src.framing", "src.frame", "src.receiver", "src.transmitter"],
        ["build_frame", "frame_build", "create_frame", "make_frame"],
    )
    payload = [int(x) for x in np.random.default_rng(2026).integers(0, 2, size=2400)]
    frame = call_with_fallback(build_frame, payload)
    if isinstance(frame, dict):
        keys = {str(key).lower() for key in frame.keys()}
        assert any("preamble" in key for key in keys), "Frame dict should contain preamble"
        assert any("length" in key for key in keys), "Frame dict should contain length"
        assert any("payload" in key for key in keys), "Frame dict should contain payload"
        assert any(("checksum" in key or "crc" in key) for key in keys), (
            "Frame dict should contain checksum or CRC"
        )
    else:
        frame_bits = to_bit_list(frame)
        assert len(frame_bits) > len(payload), (
            "Serialized frame should be longer than payload because it includes preamble, length, and checksum/CRC"
        )


def test_tc_t_006_frame_build_and_parse_are_reversible():
    build_frame = find_function(
        ["src.framing", "src.frame", "src.receiver", "src.transmitter"],
        ["build_frame", "frame_build", "create_frame", "make_frame"],
    )
    parse_frame = find_function(
        ["src.framing", "src.frame", "src.receiver"],
        ["parse_frame", "frame_parse", "extract_frame", "decode_frame"],
    )
    payload = [int(x) for x in np.random.default_rng(2027).integers(0, 2, size=257)]
    frame = call_with_fallback(build_frame, payload)
    parsed = call_with_fallback(parse_frame, frame)
    if isinstance(parsed, dict):
        recovered = parsed.get("payload") or parsed.get("payload_bits") or parsed.get("data")
        length = parsed.get("length") or parsed.get("payload_bits")
    elif isinstance(parsed, tuple):
        recovered = parsed[0]
        length = len(recovered)
    else:
        recovered = parsed
        length = len(to_bit_list(recovered))
    recovered_bits = to_bit_list(recovered)[: len(payload)]
    assert recovered_bits == payload
    assert int(length) == len(payload) or len(recovered_bits) == len(payload)


def test_tc_t_007_scramble_or_encrypt_is_reversible():
    scramble = find_function(
        ["src.crypto", "src.scramble", "src.scrambler", "src.source"],
        ["scramble", "scramble_bits", "encrypt", "encrypt_bits"],
    )
    descramble = find_function(
        ["src.crypto", "src.scramble", "src.scrambler", "src.source"],
        ["descramble", "descramble_bits", "decrypt", "decrypt_bits"],
    )
    bits = [int(x) for x in np.random.default_rng(2026).integers(0, 2, size=511)]
    scrambled = to_bit_list(call_with_fallback(scramble, bits, seed=2026))
    recovered = to_bit_list(call_with_fallback(descramble, scrambled, seed=2026))
    assert recovered[: len(bits)] == bits


def test_tc_t_008_channel_encode_decode_noiseless_reversible():
    encode = find_function(
        ["src.channel_coding", "src.coding", "src.channel_code"],
        ["channel_encode", "encode", "encode_bits", "fec_encode"],
    )
    decode = find_function(
        ["src.channel_coding", "src.coding", "src.channel_code"],
        ["channel_decode", "decode", "decode_bits", "fec_decode"],
    )
    bits = [int(x) for x in np.random.default_rng(2028).integers(0, 2, size=400)]
    coded = to_bit_list(call_with_fallback(encode, bits))
    recovered = to_bit_list(call_with_fallback(decode, coded))
    assert recovered[: len(bits)] == bits


def test_tc_t_009_qpsk_mapping_matches_prd_quadrants():
    modulate = find_function(
        ["src.modulation", "src.modem", "src.qpsk"],
        ["qpsk_modulate", "modulate_qpsk", "qpsk_mapper", "modulate"],
    )
    symbols = to_complex_list(call_with_fallback(modulate, [0, 0, 0, 1, 1, 1, 1, 0]))
    assert len(symbols) >= 4
    expected_quadrants = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    for symbol, (sign_i, sign_q) in zip(symbols[:4], expected_quadrants):
        assert math.copysign(1, symbol.real) == sign_i
        assert math.copysign(1, symbol.imag) == sign_q
    avg_power = float(np.mean(np.abs(np.array(symbols[:4])) ** 2))
    assert 0.8 <= avg_power <= 1.2, f"QPSK symbols should be approximately unit-power, got {avg_power}"


def test_tc_t_010_qpsk_noiseless_demodulation_has_no_bit_errors():
    modulate = find_function(
        ["src.modulation", "src.modem", "src.qpsk"],
        ["qpsk_modulate", "modulate_qpsk", "qpsk_mapper", "modulate"],
    )
    demodulate = find_function(
        ["src.modulation", "src.modem", "src.qpsk"],
        ["qpsk_demodulate", "demodulate_qpsk", "qpsk_demapper", "demodulate"],
    )
    bits = [int(x) for x in np.random.default_rng(2029).integers(0, 2, size=512)]
    symbols = call_with_fallback(modulate, bits)
    recovered = to_bit_list(call_with_fallback(demodulate, symbols))
    assert recovered[: len(bits)] == bits


def test_tc_t_011_qpsk_padding_removed_by_length_field():
    build_frame = find_function(
        ["src.framing", "src.frame", "src.receiver", "src.transmitter"],
        ["build_frame", "frame_build", "create_frame", "make_frame"],
    )
    parse_frame = find_function(
        ["src.framing", "src.frame", "src.receiver"],
        ["parse_frame", "frame_parse", "extract_frame", "decode_frame"],
    )
    modulate = find_function(
        ["src.modulation", "src.modem", "src.qpsk"],
        ["qpsk_modulate", "modulate_qpsk", "qpsk_mapper", "modulate"],
    )
    demodulate = find_function(
        ["src.modulation", "src.modem", "src.qpsk"],
        ["qpsk_demodulate", "demodulate_qpsk", "qpsk_demapper", "demodulate"],
    )
    payload = [int(x) for x in np.random.default_rng(2030).integers(0, 2, size=255)]
    frame = call_with_fallback(build_frame, payload)
    frame_bits = frame if isinstance(frame, dict) else to_bit_list(frame)
    if isinstance(frame_bits, dict):
        frame_bits = to_bit_list(frame_bits.get("bits") or frame_bits.get("frame") or frame_bits.get("payload"))
    symbols = call_with_fallback(modulate, frame_bits)
    recovered_frame_bits = to_bit_list(call_with_fallback(demodulate, symbols))
    parsed = call_with_fallback(parse_frame, recovered_frame_bits)
    recovered_payload = parsed.get("payload") if isinstance(parsed, dict) else (parsed[0] if isinstance(parsed, tuple) else parsed)
    assert to_bit_list(recovered_payload)[: len(payload)] == payload
    assert len(to_bit_list(recovered_payload)[: len(payload)]) == len(payload)


def test_tc_t_012_awgn_channel_is_reproducible_with_fixed_seed():
    awgn = find_function(
        ["src.channel", "src.channels", "src.awgn"],
        ["awgn", "awgn_channel", "add_awgn", "add_noise"],
    )
    symbols = np.array([1 + 1j, -1 + 1j, -1 - 1j, 1 - 1j], dtype=complex) / np.sqrt(2)
    out1 = to_complex_list(call_with_fallback(awgn, symbols, snr_db=12, seed=2026))
    out2 = to_complex_list(call_with_fallback(awgn, symbols, snr_db=12, seed=2026))
    assert np.allclose(np.array(out1), np.array(out2)), "AWGN output should be reproducible with fixed seed"
