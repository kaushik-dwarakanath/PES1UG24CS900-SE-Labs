"""Decision outcomes, short-circuit cases, and boundaries for phone repairs."""

import pytest

from phone_repair_quote import repair_days, repair_quote, trade_in_value


@pytest.mark.parametrize("express,index", [(False, 0), (True, 1)])
@pytest.mark.parametrize(
    "part,tier,warranty,totals",
    [
        ("screen", "budget", False, (4600, 5100)),
        ("screen", "budget", True, (4600, 5100)),
        ("screen", "flagship", False, (8600, 9100)),
        ("screen", "flagship", True, (8600, 9100)),
        ("battery", "budget", False, (1800, 2300)),
        ("battery", "budget", True, (300, 800)),
        ("battery", "flagship", False, (3300, 3800)),
        ("battery", "flagship", True, (300, 800)),
        ("camera", "budget", False, (2800, 3300)),
        ("camera", "budget", True, (300, 800)),
        ("camera", "flagship", False, (5300, 5800)),
        ("camera", "flagship", True, (300, 800)),
        ("charging_port", "budget", False, (1100, 1600)),
        ("charging_port", "budget", True, (300, 800)),
        ("charging_port", "flagship", False, (1900, 2400)),
        ("charging_port", "flagship", True, (300, 800)),
    ],
)
def test_quote_combinations(part, tier, warranty, totals, express, index):
    assert repair_quote(part, tier, warranty, express) == totals[index]


@pytest.mark.parametrize(
    "part,tier,message",
    [
        ("speaker", "budget", "unknown part"),
        ("", "budget", "unknown part"),
        ("Screen", "budget", "unknown part"),
        ("battery", "premium", "unknown brand tier"),
        ("battery", "", "unknown brand tier"),
        ("battery", "Flagship", "unknown brand tier"),
        ("speaker", "premium", "unknown part"),
    ],
)
def test_quote_validation_and_precedence(part, tier, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        repair_quote(part, tier, False, False)


@pytest.mark.parametrize("technicians,index", [(0, 0), (1, 1), (2, 1)])
@pytest.mark.parametrize(
    "part,in_stock,days",
    [
        ("screen", True, (3, 1)),
        ("camera", True, (3, 1)),
        ("battery", True, (3, 1)),
        ("charging_port", True, (3, 1)),
        ("screen", False, (8, 6)),
        ("camera", False, (8, 6)),
        ("battery", False, (5, 3)),
        ("charging_port", False, (5, 3)),
    ],
)
def test_turnaround_combinations(part, in_stock, days, technicians, index):
    assert repair_days(part, in_stock, technicians) == days[index]


@pytest.mark.parametrize("cracked,index", [(False, 0), (True, 1)])
@pytest.mark.parametrize(
    "age,values",
    [
        (0, (6000, 3000)),
        (1, (6000, 3000)),
        (11, (6000, 3000)),
        (12, (6000, 3000)),
        (13, (4000, 2000)),
        (23, (4000, 2000)),
        (24, (4000, 2000)),
        (25, (2000, 1000)),
        (47, (2000, 1000)),
        (48, (2000, 1000)),
        (49, (0, 0)),
        (60, (0, 0)),
    ],
)
def test_trade_in_boundaries(age, values, cracked, index):
    assert trade_in_value(10000, age, cracked) == values[index]


@pytest.mark.parametrize("cracked,index", [(False, 0), (True, 1)])
@pytest.mark.parametrize(
    "price,age,values",
    [
        (1, 0, (0, 0)),
        (1, 13, (0, 0)),
        (1, 25, (0, 0)),
        (101, 0, (60, 30)),
        (101, 13, (40, 20)),
        (101, 25, (20, 10)),
        (9999, 0, (5999, 2999)),
        (9999, 13, (3999, 1999)),
        (9999, 25, (1999, 999)),
    ],
)
def test_trade_in_integer_rounding(price, age, values, cracked, index):
    assert trade_in_value(price, age, cracked) == values[index]


@pytest.mark.parametrize("cracked", [False, True])
@pytest.mark.parametrize(
    "price,age",
    [(0, 0), (-1, 12), (10000, -1), (0, -1), (0, 49)],
)
def test_trade_in_invalid_inputs(price, age, cracked):
    # Includes each side of the validation OR and validation before early return.
    with pytest.raises(ValueError, match="^invalid input$"):
        trade_in_value(price, age, cracked)
