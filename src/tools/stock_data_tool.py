"""Stock data retrieval tool for loading historical stock performance from CSV files.

Returns structured JSON with:
  - success: bool
  - ticker: requested ticker symbol
  - num_days: number of days requested
  - data_points: number of rows returned
  - data: markdown table of stock data
  - error: error message if failed
"""

from typing import Annotated
import json
import logging
import pandas as pd
import os

# Configure logger
logger = logging.getLogger(__name__)
from langchain_core.tools import tool


@tool
def stock_data_tool(
    company_ticker: Annotated[str, "The ticker symbol of the company to retrieve their stock performance data."],
    num_days: Annotated[int, "The number of business days of stock data required to respond to the user query."]
) -> str:
    """
    Use this to look-up stock performance data for companies to retrieve a table from a CSV.
    You may need to convert company names into ticker symbols to call this function,
    e.g, Apple Inc. -> AAPL, and you may need to convert weeks, months, and years, into days.

    Available companies: Apple (AAPL), Amazon (AMZN), Meta (META), Microsoft (MSFT),
    Netflix (NFLX), Tesla (TSLA)

    Returns a JSON string with structured fields for programmatic parsing.
    """
    logger.info(f"[STOCK_DATA_TOOL] Input: company_ticker='{company_ticker}', num_days={num_days}")
    
    result = {
        "success": False,
        "ticker": company_ticker.upper(),
        "num_days": num_days,
        "data_points": 0,
        "data": None,
        "error": None,
        "price_range": None,
    }

    # Load the CSV for the company requested
    # Normalize to uppercase to handle case-insensitive lookups
    ticker_upper = company_ticker.upper()
    file_path = f"data/{ticker_upper}.csv"

    if not os.path.exists(file_path):
        result["error"] = f"Data for company {ticker_upper} is not available. Available: AAPL, AMZN, META, MSFT, NFLX, TSLA"
        return json.dumps(result)

    try:
        stock_df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

        # Rename column 'Close/Last' to 'Close' for consistency
        if 'Close/Last' in stock_df.columns:
            stock_df = stock_df.rename(columns={'Close/Last': 'Close'})

        # Clean numeric columns - remove $ and convert to float
        numeric_columns = ['Close', 'Open', 'High', 'Low']
        for col in numeric_columns:
            if col in stock_df.columns:
                stock_df[col] = stock_df[col].replace(r'[\$,]', '', regex=True).astype(float)

        # Ensure the index is in date format
        stock_df.index = stock_df.index.date

        # Maximum num_days supported by the dataset
        max_num_days = (stock_df.index.max() - stock_df.index.min()).days

        if num_days > max_num_days:
            result["error"] = f"Time period ({num_days} days) exceeds available data ({max_num_days} days)"
            return json.dumps(result)

        # Get the most recent date in the DataFrame
        final_date = stock_df.index.max()

        # Filter the DataFrame to get the last num_days of stock data
        filtered_df = stock_df[stock_df.index > (final_date - pd.Timedelta(days=num_days))]

        if len(filtered_df) == 0:
            result["error"] = "No data found for the specified period"
            logger.warning(f"[STOCK_DATA_TOOL] No data found for {company_ticker} in last {num_days} days")
            return json.dumps(result)

        result["success"] = True
        result["data_points"] = len(filtered_df)
        result["data"] = filtered_df.to_markdown()
        result["price_range"] = {
            "min": float(filtered_df['Close'].min()),
            "max": float(filtered_df['Close'].max()),
            "latest": float(filtered_df['Close'].iloc[-1])
        }
        logger.info(f"[STOCK_DATA_TOOL] Success: Retrieved {len(filtered_df)} data points for {company_ticker}")

    except Exception as e:
        result["error"] = f"Error loading data: {repr(e)}"
        logger.error(f"[STOCK_DATA_TOOL] Error for {company_ticker}: {e}")

    logger.info(f"[STOCK_DATA_TOOL] Output: success={result['success']}, data_points={result['data_points']}")
    return json.dumps(result)
