def format_currency(amount: float, currency: str = "FJD") -> str:
    """Format numerical currency values."""
    return f"{currency} {amount:,.2f}"