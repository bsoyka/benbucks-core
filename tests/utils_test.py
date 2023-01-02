import pytest

from benbucks_core._utils import CURRENCY_SYMBOL, _format_money, _round_money


@pytest.mark.parametrize(
    "test_input,expected",
    {(1, 1), (1.23, 1.23), (1.2344444444, 1.23), (1.2355555555, 1.24)},
)
def test_round_currency(test_input: int | float, expected: int | float):
    """Test rounding to two decimal places."""
    assert _round_money(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    {(1.0, 1), (1, 1), (0.999999999, 1), (1.00000001, 1)},
)
def test_round_currency_type(test_input: int | float, expected: int | float):
    """Test result type of rounding."""
    assert type(_round_money(test_input)) == type(expected)


@pytest.mark.parametrize(
    "test_input,expected",
    {
        (1, "1.00"),
        (1.23, "1.23"),
        (1.2344444444, "1.23"),
        (1.2355555555, "1.24"),
    },
)
def test_format_money(test_input: int | float, expected: str):
    """Test formatting of currency."""
    assert _format_money(test_input) == CURRENCY_SYMBOL + expected
