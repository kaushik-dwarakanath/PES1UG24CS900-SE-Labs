import pytest
from hypothesis import given, settings, strategies as st
from phone_repair_quote_parser import mask_imei, parse_parts_order, parse_model


# Include the handout's arbitrary Unicode/None inputs and other common types.
inputs = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.binary(),
    st.lists(st.integers()), st.dictionaries(st.text(), st.integers()),
)


@settings(max_examples=500)
@given(inputs)
def test_mask_imei_no_crash(s):
    try:
        result = mask_imei(s)
    except Exception as exc:
        pytest.fail(f"mask_imei crashed for {s!r}: {exc!r}")
    assert isinstance(result, str)
    if not isinstance(s, str):
        assert result == ""
    else:
        cleaned = s.replace("-", "").replace(" ", "")
        if not cleaned or any(c not in "0123456789" for c in cleaned):
            assert result == ""
        else:
            visible = min(4, len(cleaned))
            assert result.endswith(cleaned[-visible:])
            assert len(result) == len(cleaned)
            assert result[:-visible] == "*" * (len(cleaned) - visible)


@settings(max_examples=500)
@given(st.one_of(inputs, st.builds(
    lambda part, qty: f"{part} x{qty}",
    st.sampled_from(["screen", "battery", "flex cable", "box"]),
    st.integers(min_value=1, max_value=10000),
)))
def test_parse_parts_order_no_crash(s):
    try:
        result = parse_parts_order(s)
    except Exception as exc:
        pytest.fail(f"parse_parts_order crashed for {s!r}: {exc!r}")
    assert isinstance(result, dict)
    assert all(isinstance(part, str) and part and part == part.strip()
               and isinstance(qty, int) and qty > 0
               for part, qty in result.items())
    if not isinstance(s, str):
        assert result == {}


@settings(max_examples=500)
@given(inputs)
def test_parse_model_no_crash(s):
    try:
        result = parse_model(s)
    except Exception as exc:
        pytest.fail(f"parse_model crashed for {s!r}: {exc!r}")
    assert isinstance(result, tuple) and len(result) == 2
    assert all(isinstance(value, str) for value in result)
    words = s.split() if isinstance(s, str) else []
    expected = (words[0].title(), " ".join(words[1:])) if words else ("", "")
    assert result == expected


@pytest.mark.parametrize("function,value,expected", [
    (mask_imei, "35-209900-176148-1", "***********1481"),
    (mask_imei, "1234", "1234"),
    (mask_imei, "12", "12"),
    (mask_imei, " - ", ""),
    (mask_imei, "abc1234", ""),
    (mask_imei, "１２３４", ""),
    (mask_imei, 123456, ""),
    (parse_parts_order, "screen x1; battery x2", {"screen": 1, "battery": 2}),
    (parse_parts_order, "box x2; flex cable x3", {"box": 2, "flex cable": 3}),
    (parse_parts_order, "screen x1; broken; battery x2;", {"screen": 1, "battery": 2}),
    (parse_parts_order, "screen x1; screen x3", {"screen": 3}),
    (parse_parts_order, "x2; camera x0; screen x-1; battery xno", {}),
    (parse_parts_order, "screen x1.5; battery x²; camera x1x2", {}),
    (parse_parts_order, "screen x" + "9" * 5000, {}),
    (parse_parts_order, None, {}),
    (parse_model, "Samsung Galaxy S23", ("Samsung", "Galaxy S23")),
    (parse_model, "  samsung\tGalaxy   S23  ", ("Samsung", "Galaxy S23")),
    (parse_model, "Samsung", ("Samsung", "")),
    (parse_model, "  ", ("", "")),
    (parse_model, None, ("", "")),
])
def test_regressions(function, value, expected):
    assert function(value) == expected
