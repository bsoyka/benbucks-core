CURRENCY_SYMBOL = "\u20bf"


def _round_money(amount: int | float) -> int | float:
    """Round a currency amount to the nearest cent."""
    rounded = round(amount, 2)

    # If the rounded value is an integer, return it as an int
    return int(rounded) if rounded == int(rounded) else rounded


def _format_money(amount: int | float) -> str:
    """Format a currency amount as a string."""
    return f"{CURRENCY_SYMBOL}{_round_money(amount):.2f}"
