"""Statement coverage tests for the phone repair application."""

import pytest

from phone_repair_quote import repair_days, repair_quote, trade_in_value


@pytest.mark.parametrize(
    "part,tier,warranty,express,expected",
    [
        ("screen", "budget", False, False, 4600),
        ("battery", "flagship", True, True, 800),
        ("camera", "flagship", False, False, 5300),
        ("charging_port", "budget", False, False, 1100),
    ],
)
def test_repair_prices(part, tier, warranty, express, expected):
    assert repair_quote(part, tier, warranty, express) == expected


@pytest.mark.parametrize(
    "part,tier,message",
    [
        ("speaker", "budget", "unknown part"),
        ("battery", "premium", "unknown brand tier"),
    ],
)
def test_invalid_repair(part, tier, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        repair_quote(part, tier, False, False)


@pytest.mark.parametrize(
    "part,in_stock,technicians,expected",
    [
        ("battery", True, 2, 1),
        ("screen", False, 0, 8),
        ("charging_port", False, 1, 3),
    ],
)
def test_turnaround(part, in_stock, technicians, expected):
    assert repair_days(part, in_stock, technicians) == expected


@pytest.mark.parametrize(
    "price,age,cracked,expected",
    [
        (10000, 12, False, 6000),
        (10000, 24, False, 4000),
        (10000, 48, True, 1000),
        (10000, 49, False, 0),
    ],
)
def test_trade_in_prices(price, age, cracked, expected):
    assert trade_in_value(price, age, cracked) == expected


def test_invalid_trade_in_price():
    with pytest.raises(ValueError, match="^invalid input$"):
        trade_in_value(0, 12, False)
