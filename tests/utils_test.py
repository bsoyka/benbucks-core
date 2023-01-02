import pytest

from benbucks_core._utils import CURRENCY_SYMBOL, format_money


@pytest.mark.parametrize(
    "test_input,expected",
    {
        (1.0, "1.00"),
        (1.23, "1.23"),
        (1.2344444444, "1.23"),
        (1.2355555555, "1.24"),
    },
)
def test_format_money(test_input: float, expected: str):
    """Test formatting of currency."""
    assert format_money(test_input) == CURRENCY_SYMBOL + expected
