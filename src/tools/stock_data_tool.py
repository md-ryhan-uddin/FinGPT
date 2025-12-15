"""Stock data retrieval tool for loading historical stock performance from CSV files."""

from typing import Annotated
import pandas as pd
import os
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
    """

    # Load the CSV for the company requested
    file_path = f"data/{company_ticker}.csv"

    if os.path.exists(file_path) is False:
        return f"Sorry, but data for company {company_ticker} is not available. Please try Apple (AAPL), Amazon (AMZN), Meta (META), Microsoft (MSFT), Netflix (NFLX), or Tesla (TSLA)."

    stock_df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

    # Rename column 'Close/Last' to 'Close' for consistency
    if 'Close/Last' in stock_df.columns:
        stock_df = stock_df.rename(columns={'Close/Last': 'Close'})

    # Clean numeric columns - remove $ and convert to float
    numeric_columns = ['Close', 'Open', 'High', 'Low']
    for col in numeric_columns:
        if col in stock_df.columns:
            stock_df[col] = stock_df[col].replace('[\$,]', '', regex=True).astype(float)

    # Ensure the index is in date format
    stock_df.index = stock_df.index.date

    # Maximum num_days supported by the dataset
    max_num_days = (stock_df.index.max() - stock_df.index.min()).days

    if num_days > max_num_days:
        return "Sorry, but this time period exceeds the data available. Please reduce it to continue."

    # Get the most recent date in the DataFrame
    final_date = stock_df.index.max()

    # Filter the DataFrame to get the last num_days of stock data
    filtered_df = stock_df[stock_df.index > (final_date - pd.Timedelta(days=num_days))]

    return f"Successfully executed the stock performance data retrieval tool to retrieve the last *{num_days} days* of data for company **{company_ticker}**:\n\n{filtered_df.to_markdown()}"
