CURRENCY_SYMBOL = "\u20bf"


def format_money(amount: float) -> str:
    """Format a currency amount as a string."""
    return f"{CURRENCY_SYMBOL}{round(amount, 2):.2f}"
