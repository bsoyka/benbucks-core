def _round_money(prize: int | float) -> int | float:
    """Round a currency amount to the nearest cent."""
    rounded = round(prize, 2)

    # If the rounded value is an integer, return it as an int
    return int(rounded) if rounded == int(rounded) else rounded
