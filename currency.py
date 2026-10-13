"""
Currency conversion for Mizan.

Mizan scores merchants in Algeria, Nigeria and South Africa, so every money
value needs to be readable in all three currencies. We convert through the
US dollar: any currency -> USD -> any other currency. That way each new
country only needs one rate instead of a rate against every other currency.
"""

SUPPORTED_CURRENCIES = ("DZD", "NGN", "ZAR")

# How many units of each currency equal one US dollar.
# These are reference rates used as the starting point. The app lets the
# user change them, because exchange rates move and Algeria in particular
# has a gap between the official and the street rate.
DEFAULT_RATES_PER_USD = {
    "DZD": 132.0,
    "NGN": 1500.0,
    "ZAR": 17.5,
}


def convert(amount, from_currency, to_currency, rates=None):
    """Convert an amount from one supported currency to another."""
    rates = rates or DEFAULT_RATES_PER_USD

    for code in (from_currency, to_currency):
        if code not in rates:
            raise ValueError(f"Unsupported currency: {code}")
        if rates[code] <= 0:
            raise ValueError(f"Exchange rate for {code} must be positive")

    if from_currency == to_currency:
        return float(amount)

    amount_in_usd = amount / rates[from_currency]
    return amount_in_usd * rates[to_currency]


def convert_to_all(amount, from_currency, rates=None):
    """Return the same amount expressed in every supported currency."""
    return {
        code: convert(amount, from_currency, code, rates)
        for code in SUPPORTED_CURRENCIES
    }


def format_amount(amount, currency):
    """Write an amount the way people read it, e.g. '1,250,000.00 DZD'."""
    return f"{amount:,.2f} {currency}"


if __name__ == "__main__":
    # Quick check you can run by hand: python currency.py
    monthly_cash_flow = 1_000_000
    print(f"Converting {format_amount(monthly_cash_flow, 'DZD')}:")
    for code, value in convert_to_all(monthly_cash_flow, "DZD").items():
        print(f"  {format_amount(value, code)}")

    there_and_back = convert(convert(250_000, "DZD", "NGN"), "NGN", "DZD")
    print(f"Round trip DZD -> NGN -> DZD: {there_and_back:,.2f}")