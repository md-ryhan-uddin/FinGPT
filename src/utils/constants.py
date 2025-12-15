"""Constants for FinGPT application."""

# Available stock tickers
AVAILABLE_TICKERS = ["AAPL", "AMZN", "META", "MSFT", "NFLX", "TSLA"]

# Company name to ticker mapping
COMPANY_TO_TICKER = {
    "apple": "AAPL",
    "amazon": "AMZN",
    "meta": "META",
    "facebook": "META",
    "microsoft": "MSFT",
    "netflix": "NFLX",
    "tesla": "TSLA",
}

# Time period conversions (approximate trading days)
TIME_PERIODS = {
    "week": 7,
    "month": 30,
    "quarter": 90,
    "6 months": 180,
    "year": 365,
}
