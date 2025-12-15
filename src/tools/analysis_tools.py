"""Statistical analysis tools for quantitative financial analysis."""

from typing import Annotated
import pandas as pd
import numpy as np
import os
from langchain_core.tools import tool


@tool
def calculate_returns_tool(
    company_ticker: Annotated[str, "The ticker symbol of the company (e.g., AAPL, TSLA)"],
    num_days: Annotated[int, "Number of days to calculate returns for"]
) -> str:
    """
    Calculate daily and cumulative returns for a stock over a specified period.
    Returns percentage changes and total return over the period.
    """
    file_path = f"data/{company_ticker}.csv"

    if not os.path.exists(file_path):
        return f"Data for {company_ticker} not available. Available: AAPL, AMZN, META, MSFT, NFLX, TSLA"

    try:
        df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

        # Rename column 'Close/Last' to 'Close' for consistency
        if 'Close/Last' in df.columns:
            df = df.rename(columns={'Close/Last': 'Close'})

        # Clean numeric columns - remove $ and convert to float
        numeric_columns = ['Close', 'Open', 'High', 'Low']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)

        df.index = df.index.date

        final_date = df.index.max()
        filtered_df = df[df.index > (final_date - pd.Timedelta(days=num_days))]

        if len(filtered_df) < 2:
            return "Insufficient data for the specified period"

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

        result = f"""**Returns Analysis for {company_ticker}** ({num_days} days):

- **Total Return**: {total_return:.2f}%
- **Average Daily Return**: {avg_daily_return:.2f}%
- **Best Day**: +{max_daily_gain:.2f}%
- **Worst Day**: {max_daily_loss:.2f}%
- **Starting Price**: ${start_price:.2f}
- **Ending Price**: ${end_price:.2f}
"""
        return result

    except Exception as e:
        return f"Error calculating returns: {str(e)}"


@tool
def calculate_volatility_tool(
    company_ticker: Annotated[str, "The ticker symbol of the company"],
    num_days: Annotated[int, "Number of days to analyze volatility"]
) -> str:
    """
    Calculate volatility (standard deviation of returns) for a stock.
    Higher volatility indicates higher risk.
    """
    file_path = f"data/{company_ticker}.csv"

    if not os.path.exists(file_path):
        return f"Data for {company_ticker} not available."

    try:
        df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

        # Rename column 'Close/Last' to 'Close' for consistency
        if 'Close/Last' in df.columns:
            df = df.rename(columns={'Close/Last': 'Close'})

        # Clean numeric columns - remove $ and convert to float
        numeric_columns = ['Close', 'Open', 'High', 'Low']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)

        df.index = df.index.date

        final_date = df.index.max()
        filtered_df = df[df.index > (final_date - pd.Timedelta(days=num_days))]

        if len(filtered_df) < 2:
            return "Insufficient data"

        # Calculate daily returns
        daily_returns = filtered_df['Close'].pct_change().dropna()

        # Calculate volatility (standard deviation)
        volatility = daily_returns.std() * 100

        # Annualized volatility (assuming 252 trading days per year)
        annualized_volatility = volatility * np.sqrt(252)

        result = f"""**Volatility Analysis for {company_ticker}** ({num_days} days):

- **Daily Volatility**: {volatility:.2f}%
- **Annualized Volatility**: {annualized_volatility:.2f}%

*Interpretation: Higher volatility = higher risk/reward potential*
"""
        return result

    except Exception as e:
        return f"Error calculating volatility: {str(e)}"


@tool
def compare_stocks_tool(
    ticker1: Annotated[str, "First company ticker symbol"],
    ticker2: Annotated[str, "Second company ticker symbol"],
    num_days: Annotated[int, "Number of days to compare"]
) -> str:
    """
    Compare performance metrics between two stocks over a specified period.
    Returns side-by-side comparison of returns and volatility.
    """
    results = []

    for ticker in [ticker1, ticker2]:
        file_path = f"data/{ticker}.csv"
        if not os.path.exists(file_path):
            return f"Data for {ticker} not available."

        try:
            df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

            # Rename column 'Close/Last' to 'Close' for consistency
            if 'Close/Last' in df.columns:
                df = df.rename(columns={'Close/Last': 'Close'})

            # Clean numeric columns - remove $ and convert to float
            numeric_columns = ['Close', 'Open', 'High', 'Low']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)

            df.index = df.index.date

            final_date = df.index.max()
            filtered_df = df[df.index > (final_date - pd.Timedelta(days=num_days))]

            if len(filtered_df) < 2:
                return f"Insufficient data for {ticker}"

            # Calculate metrics
            daily_returns = filtered_df['Close'].pct_change().dropna()
            start_price = filtered_df['Close'].iloc[0]
            end_price = filtered_df['Close'].iloc[-1]
            total_return = ((end_price - start_price) / start_price) * 100
            volatility = daily_returns.std() * 100
            avg_return = daily_returns.mean() * 100

            results.append({
                'ticker': ticker,
                'total_return': total_return,
                'avg_daily_return': avg_return,
                'volatility': volatility,
                'start_price': start_price,
                'end_price': end_price
            })

        except Exception as e:
            return f"Error analyzing {ticker}: {str(e)}"

    # Compare
    r1, r2 = results[0], results[1]

    comparison = f"""**Comparative Analysis: {ticker1} vs {ticker2}** ({num_days} days)

**{ticker1}:**
- Total Return: {r1['total_return']:.2f}%
- Avg Daily Return: {r1['avg_daily_return']:.2f}%
- Volatility: {r1['volatility']:.2f}%
- Price: ${r1['start_price']:.2f} → ${r1['end_price']:.2f}

**{ticker2}:**
- Total Return: {r2['total_return']:.2f}%
- Avg Daily Return: {r2['avg_daily_return']:.2f}%
- Volatility: {r2['volatility']:.2f}%
- Price: ${r2['start_price']:.2f} → ${r2['end_price']:.2f}

**Winner:**
- Better Return: {ticker1 if r1['total_return'] > r2['total_return'] else ticker2} ({max(r1['total_return'], r2['total_return']):.2f}%)
- Lower Risk: {ticker1 if r1['volatility'] < r2['volatility'] else ticker2} ({min(r1['volatility'], r2['volatility']):.2f}% volatility)
"""
    return comparison


@tool
def correlation_analysis_tool(
    tickers_list: Annotated[str, "Comma-separated list of ticker symbols (e.g., 'AAPL,MSFT,TSLA')"],
    num_days: Annotated[int, "Number of days to analyze"]
) -> str:
    """
    Calculate correlation matrix between multiple stocks.
    Shows how stocks move together (1.0 = perfect correlation, -1.0 = inverse correlation).
    """
    tickers = [t.strip() for t in tickers_list.split(',')]

    if len(tickers) < 2:
        return "Please provide at least 2 ticker symbols"

    returns_data = {}

    for ticker in tickers:
        file_path = f"data/{ticker}.csv"
        if not os.path.exists(file_path):
            return f"Data for {ticker} not available."

        try:
            df = pd.read_csv(file_path, index_col='Date', parse_dates=True)

            # Rename column 'Close/Last' to 'Close' for consistency
            if 'Close/Last' in df.columns:
                df = df.rename(columns={'Close/Last': 'Close'})

            # Clean numeric columns - remove $ and convert to float
            numeric_columns = ['Close', 'Open', 'High', 'Low']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = df[col].replace('[\$,]', '', regex=True).astype(float)

            df.index = df.index.date

            final_date = df.index.max()
            filtered_df = df[df.index > (final_date - pd.Timedelta(days=num_days))]

            daily_returns = filtered_df['Close'].pct_change().dropna()
            returns_data[ticker] = daily_returns

        except Exception as e:
            return f"Error loading {ticker}: {str(e)}"

    # Create DataFrame and calculate correlation
    returns_df = pd.DataFrame(returns_data)
    correlation_matrix = returns_df.corr()

    result = f"""**Correlation Analysis** ({num_days} days):

{correlation_matrix.to_markdown()}

*Interpretation:*
- 1.0 = Perfect positive correlation (move together)
- 0.0 = No correlation
- -1.0 = Perfect negative correlation (move opposite)
"""
    return result
