"""Statistical analysis tools for quantitative financial analysis.

All tools return structured JSON with success/error fields for programmatic parsing.
"""

from typing import Annotated
import json
import logging
import pandas as pd
import numpy as np
import os
from langchain_core.tools import tool

# Configure logger
logger = logging.getLogger(__name__)


@tool
def calculate_returns_tool(
    company_ticker: Annotated[str, "The ticker symbol of the company (e.g., AAPL, TSLA)"],
    num_days: Annotated[int, "Number of days to calculate returns for"]
) -> str:
    """
    Calculate daily and cumulative returns for a stock over a specified period.
    Returns percentage changes and total return over the period.
    
    Returns JSON with success, ticker, metrics (total_return, avg_daily_return, etc.), and error fields.
    """
    logger.info(f"[CALCULATE_RETURNS] Input: ticker={company_ticker}, num_days={num_days}")
    
    result = {
        "success": False,
        "ticker": company_ticker.upper(),
        "num_days": num_days,
        "metrics": None,
        "error": None
    }
    
    file_path = f"data/{company_ticker.upper()}.csv"

    if not os.path.exists(file_path):
        result["error"] = f"Data for {company_ticker} not available. Available: AAPL, AMZN, META, MSFT, NFLX, TSLA"
        return json.dumps(result)

    try:
        df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

        # Rename column 'Close/Last' to 'Close' for consistency
        if 'Close/Last' in df.columns:
            df = df.rename(columns={'Close/Last': 'Close'})

        # Clean numeric columns - remove $ and convert to float
        numeric_columns = ['Close', 'Open', 'High', 'Low']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].replace(r'[\$,]', '', regex=True).astype(float)

        df.index = df.index.date

        final_date = df.index.max()
        filtered_df = df[df.index > (final_date - pd.Timedelta(days=num_days))]

        if len(filtered_df) < 2:
            result["error"] = "Insufficient data for the specified period (need at least 2 data points)"
            return json.dumps(result)

        # Calculate daily returns
        daily_returns = filtered_df['Close'].pct_change() * 100

        # Calculate cumulative return
        start_price = filtered_df['Close'].iloc[0]
        end_price = filtered_df['Close'].iloc[-1]
        total_return = ((end_price - start_price) / start_price) * 100

        # Statistics
        avg_daily_return = daily_returns.mean()
        max_daily_gain = daily_returns.max()
        max_daily_loss = daily_returns.min()

        result["success"] = True
        result["metrics"] = {
            "total_return": round(float(total_return), 2),
            "avg_daily_return": round(float(avg_daily_return), 2),
            "max_daily_gain": round(float(max_daily_gain), 2),
            "max_daily_loss": round(float(max_daily_loss), 2),
            "start_price": round(float(start_price), 2),
            "end_price": round(float(end_price), 2),
            "data_points": len(filtered_df)
        }

    except Exception as e:
        result["error"] = f"Error calculating returns: {repr(e)}"

    return json.dumps(result)


@tool
def calculate_volatility_tool(
    company_ticker: Annotated[str, "The ticker symbol of the company"],
    num_days: Annotated[int, "Number of days to analyze volatility"]
) -> str:
    """
    Calculate volatility (standard deviation of returns) for a stock.
    Higher volatility indicates higher risk.
    
    Returns JSON with success, ticker, volatility metrics, and error fields.
    """
    logger.info(f"[CALCULATE_VOLATILITY] Input: ticker={company_ticker}, num_days={num_days}")
    result = {
        "success": False,
        "ticker": company_ticker.upper(),
        "num_days": num_days,
        "metrics": None,
        "error": None
    }
    
    file_path = f"data/{company_ticker.upper()}.csv"

    if not os.path.exists(file_path):
        result["error"] = f"Data for {company_ticker} not available. Available: AAPL, AMZN, META, MSFT, NFLX, TSLA"
        return json.dumps(result)

    try:
        df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

        # Rename column 'Close/Last' to 'Close' for consistency
        if 'Close/Last' in df.columns:
            df = df.rename(columns={'Close/Last': 'Close'})

        # Clean numeric columns - remove $ and convert to float
        numeric_columns = ['Close', 'Open', 'High', 'Low']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].replace(r'[\$,]', '', regex=True).astype(float)

        df.index = df.index.date

        final_date = df.index.max()
        filtered_df = df[df.index > (final_date - pd.Timedelta(days=num_days))]

        if len(filtered_df) < 2:
            result["error"] = "Insufficient data (need at least 2 data points)"
            return json.dumps(result)

        # Calculate daily returns
        daily_returns = filtered_df['Close'].pct_change().dropna()

        # Calculate volatility (standard deviation)
        volatility = daily_returns.std() * 100

        # Annualized volatility (assuming 252 trading days per year)
        annualized_volatility = volatility * np.sqrt(252)

        result["success"] = True
        result["metrics"] = {
            "daily_volatility": round(float(volatility), 2),
            "annualized_volatility": round(float(annualized_volatility), 2),
            "data_points": len(filtered_df)
        }

    except Exception as e:
        result["error"] = f"Error calculating volatility: {repr(e)}"

    return json.dumps(result)


@tool
def compare_stocks_tool(
    ticker1: Annotated[str, "First company ticker symbol"],
    ticker2: Annotated[str, "Second company ticker symbol"],
    num_days: Annotated[int, "Number of days to compare"]
) -> str:
    """
    Compare performance metrics between two stocks over a specified period.
    Returns side-by-side comparison of returns and volatility.
    
    Returns JSON with success, comparison metrics for both stocks, winner analysis, and error fields.
    """
    logger.info(f"[COMPARE_STOCKS] Input: ticker1={ticker1}, ticker2={ticker2}, num_days={num_days}")
    result = {
        "success": False,
        "ticker1": ticker1.upper(),
        "ticker2": ticker2.upper(),
        "num_days": num_days,
        "comparison": None,
        "winner": None,
        "error": None
    }
    
    stock_metrics = []

    for ticker in [ticker1, ticker2]:
        file_path = f"data/{ticker.upper()}.csv"
        if not os.path.exists(file_path):
            result["error"] = f"Data for {ticker} not available. Available: AAPL, AMZN, META, MSFT, NFLX, TSLA"
            return json.dumps(result)

        try:
            df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

            # Rename column 'Close/Last' to 'Close' for consistency
            if 'Close/Last' in df.columns:
                df = df.rename(columns={'Close/Last': 'Close'})

            # Clean numeric columns - remove $ and convert to float
            numeric_columns = ['Close', 'Open', 'High', 'Low']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = df[col].replace(r'[\$,]', '', regex=True).astype(float)

            df.index = df.index.date

            final_date = df.index.max()
            filtered_df = df[df.index > (final_date - pd.Timedelta(days=num_days))]

            if len(filtered_df) < 2:
                result["error"] = f"Insufficient data for {ticker}"
                return json.dumps(result)

            # Calculate metrics
            daily_returns = filtered_df['Close'].pct_change().dropna()
            start_price = filtered_df['Close'].iloc[0]
            end_price = filtered_df['Close'].iloc[-1]
            total_return = ((end_price - start_price) / start_price) * 100
            volatility = daily_returns.std() * 100
            avg_return = daily_returns.mean() * 100

            stock_metrics.append({
                'ticker': ticker.upper(),
                'total_return': round(float(total_return), 2),
                'avg_daily_return': round(float(avg_return), 2),
                'volatility': round(float(volatility), 2),
                'start_price': round(float(start_price), 2),
                'end_price': round(float(end_price), 2)
            })

        except Exception as e:
            result["error"] = f"Error analyzing {ticker}: {repr(e)}"
            return json.dumps(result)

    # Compare
    r1, r2 = stock_metrics[0], stock_metrics[1]
    
    result["success"] = True
    result["comparison"] = {
        ticker1.upper(): r1,
        ticker2.upper(): r2
    }
    result["winner"] = {
        "better_return": ticker1.upper() if r1['total_return'] > r2['total_return'] else ticker2.upper(),
        "better_return_value": max(r1['total_return'], r2['total_return']),
        "lower_risk": ticker1.upper() if r1['volatility'] < r2['volatility'] else ticker2.upper(),
        "lower_risk_value": min(r1['volatility'], r2['volatility'])
    }

    return json.dumps(result)


@tool
def correlation_analysis_tool(
    tickers_list: Annotated[str, "Comma-separated list of ticker symbols (e.g., 'AAPL,MSFT,TSLA')"],
    num_days: Annotated[int, "Number of days to analyze"]
) -> str:
    """
    Calculate correlation matrix between multiple stocks.
    Shows how stocks move together (1.0 = perfect correlation, -1.0 = inverse correlation).
    
    Returns JSON with success, tickers analyzed, correlation matrix, and error fields.
    """
    logger.info(f"[CORRELATION_ANALYSIS] Input: tickers={tickers_list}, num_days={num_days}")
    result = {
        "success": False,
        "tickers": None,
        "num_days": num_days,
        "correlation_matrix": None,
        "data": None,
        "error": None
    }
    
    tickers = [t.strip().upper() for t in tickers_list.split(',')]
    result["tickers"] = tickers

    if len(tickers) < 2:
        result["error"] = "Please provide at least 2 ticker symbols"
        return json.dumps(result)

    returns_data = {}

    for ticker in tickers:
        file_path = f"data/{ticker.upper()}.csv"
        if not os.path.exists(file_path):
            result["error"] = f"Data for {ticker} not available. Available: AAPL, AMZN, META, MSFT, NFLX, TSLA"
            return json.dumps(result)

        try:
            df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

            # Rename column 'Close/Last' to 'Close' for consistency
            if 'Close/Last' in df.columns:
                df = df.rename(columns={'Close/Last': 'Close'})

            # Clean numeric columns - remove $ and convert to float
            numeric_columns = ['Close', 'Open', 'High', 'Low']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = df[col].replace(r'[\$,]', '', regex=True).astype(float)

            df.index = df.index.date

            final_date = df.index.max()
            filtered_df = df[df.index > (final_date - pd.Timedelta(days=num_days))]

            daily_returns = filtered_df['Close'].pct_change().dropna()
            returns_data[ticker] = daily_returns

        except Exception as e:
            result["error"] = f"Error loading {ticker}: {repr(e)}"
            return json.dumps(result)

    # Create DataFrame and calculate correlation
    returns_df = pd.DataFrame(returns_data)
    correlation_matrix = returns_df.corr()

    result["success"] = True
    result["correlation_matrix"] = correlation_matrix.to_dict()
    result["data"] = correlation_matrix.to_markdown()

    return json.dumps(result)
