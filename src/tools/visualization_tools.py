"""Python execution tool for creating visualizations and running data analysis code."""

import matplotlib

# Use non-interactive backend before importing pyplot
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import contextlib
import io
import os
import shutil
import uuid
from pathlib import Path
from typing import Annotated, Optional

import pandas as pd
from langchain_core.tools import tool

from src.utils.constants import AVAILABLE_TICKERS, COMPANY_TO_TICKER

# Shared namespace so state persists across executions similar to PythonREPL
_EXEC_NAMESPACE = {"__name__": "__main__"}


def _ensure_project_root() -> Path:
    """Make sure we are running from the FinGPT project root."""
    cwd = Path.cwd()

    if cwd.name == "FinGPT":
        return cwd

    if "FinGPT" in cwd.parts:
        while cwd.name != "FinGPT" and cwd != cwd.parent:
            cwd = cwd.parent
        os.chdir(cwd)
        return cwd

    candidate = cwd / "FinGPT"
    if candidate.exists():
        os.chdir(candidate)
        return candidate

    return cwd


def _ensure_data_aliases(data_dir: Path) -> None:
    """
    Create case-insensitive aliases for CSV files so code using lowercase
    paths (e.g., data/meta.csv) still works on case-sensitive filesystems.
    """
    if not data_dir.exists():
        return

    for csv_path in data_dir.glob("*.csv"):
        alias_names = {
            csv_path.name.lower(),
            f"{csv_path.stem.capitalize()}{csv_path.suffix}",
        }
        for alias in alias_names:
            alias_path = csv_path.with_name(alias)
            if alias_path.exists() or alias_path == csv_path:
                continue
            try:
                # Prefer lightweight symlink to avoid duplicating data
                alias_path.symlink_to(csv_path.name)
            except OSError:
                # Fall back to copying if symlinks are not permitted
                try:
                    shutil.copyfile(csv_path, alias_path)
                except OSError:
                    pass


def load_stock_dataframe(ticker: str, days: Optional[int] = None) -> pd.DataFrame:
    """
    Helper available inside the execution environment to load and clean stock data.

    Args:
        ticker: Company ticker or name (case-insensitive)
        days: Optional number of most recent rows to return

    Returns:
        Cleaned pandas DataFrame with a parsed Date column and numeric prices.
    """
    ticker_key = ticker.strip()
    ticker_key = COMPANY_TO_TICKER.get(ticker_key.lower(), ticker_key.upper())

    data_dir = Path("data")
    _ensure_data_aliases(data_dir)

    csv_path = None
    for candidate in data_dir.glob("*.csv"):
        if candidate.stem.lower() == ticker_key.lower():
            csv_path = candidate
            break

    if csv_path is None:
        raise FileNotFoundError(
            f"No data file found for {ticker_key}. Available tickers: {', '.join(AVAILABLE_TICKERS)}"
        )

    df = pd.read_csv(csv_path, parse_dates=["Date"])

    price_column = "Close/Last" if "Close/Last" in df.columns else "Close"
    df["Close"] = df[price_column].replace(r"[\\$,]", "", regex=True).astype(float)
    df = df.sort_values("Date").reset_index(drop=True)

    if days:
        df = df.tail(days)

    return df


def _execute_user_code(code: str) -> str:
    """Execute arbitrary Python code and capture stdout/stderr as a string."""
    stdout = io.StringIO()
    stderr = io.StringIO()

    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exec(code, _EXEC_NAMESPACE, _EXEC_NAMESPACE)

    output = stdout.getvalue().strip()
    errors = stderr.getvalue().strip()
    return errors if errors else output


@tool
def python_repl_tool(
    code: Annotated[str, "The python code to execute to generate charts and visualizations."],
) -> str:
    """
    Use this to execute python code for creating visualizations and data analysis.

    IMPORTANT DATA FORMAT:
    - CSV files use 'Close/Last' column name (not 'Close')
    - Always check column names or use: df.rename(columns={'Close/Last': 'Close'})
    - Dollar signs ($) in prices need to be cleaned

    Available libraries: pandas, numpy, matplotlib, seaborn
    Note: Charts will be automatically saved and displayed.
    """
    try:
        _ensure_project_root()
        _ensure_data_aliases(Path("data"))

        # Make helpers available to executed code
        _EXEC_NAMESPACE.setdefault("load_stock_dataframe", load_stock_dataframe)
        _EXEC_NAMESPACE.setdefault("AVAILABLE_TICKERS", AVAILABLE_TICKERS)

        # Reset figures from any previous run
        plt.close("all")

        result = _execute_user_code(code)

        # Check if there are any matplotlib figures created
        figures = plt.get_fignums()
        saved_images = []

        if figures:
            os.makedirs("output", exist_ok=True)

            for fig_num in figures:
                fig = plt.figure(fig_num)
                filename = f"output/chart_{uuid.uuid4().hex[:8]}.png"
                fig.savefig(filename, dpi=100, bbox_inches="tight")
                saved_images.append(filename)

            plt.close("all")

            if saved_images:
                image_info = "\n\n**Charts created:**\n" + "\n".join(
                    [f"![Chart]({img})" for img in saved_images]
                )
                return (
                    "Successfully created visualization.\n\n"
                    "Chart saved and will be displayed to the user."
                    + image_info
                )

        if result and str(result).strip():
            return f"Code executed successfully.\n\nOutput:\n```\n{result}\n```"
        else:
            return "Code executed successfully (no output)."

    except BaseException as e:
        return (
            f"Failed to execute. Error: {repr(e)}\n\n"
            "Tip: Use load_stock_dataframe('TICKER', days) to reliably load CSV data."
        )
