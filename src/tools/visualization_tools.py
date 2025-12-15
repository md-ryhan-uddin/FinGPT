"""Python REPL tool for creating visualizations and executing data analysis code."""

import matplotlib
matplotlib.use('Agg')  # Set backend before importing pyplot
import matplotlib.pyplot as plt

from typing import Annotated
from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
import os
import uuid


# Create a shared REPL instance
repl = PythonREPL()


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
        # Execute the code
        result = repl.run(code)

        # Check if there are any matplotlib figures created
        figures = plt.get_fignums()
        saved_images = []

        if figures:
            # Create output directory if it doesn't exist
            os.makedirs("output", exist_ok=True)

            # Save each figure
            for fig_num in figures:
                fig = plt.figure(fig_num)
                # Generate unique filename
                filename = f"output/chart_{uuid.uuid4().hex[:8]}.png"
                fig.savefig(filename, dpi=100, bbox_inches='tight')
                saved_images.append(filename)

            # Close all figures to free memory
            plt.close('all')

            # Add image paths to output
            if saved_images:
                image_info = "\n\n**Charts created:**\n" + "\n".join([f"![Chart]({img})" for img in saved_images])
                return f"Successfully created visualization.\n\nChart saved and will be displayed to the user.{image_info}"

        # No figures created - return execution result
        if result and str(result).strip():
            return f"Code executed successfully.\n\nOutput:\n```\n{result}\n```"
        else:
            return "Code executed successfully (no output)."

    except BaseException as e:
        return f"Failed to execute. Error: {repr(e)}\n\nTip: Check column names in CSV. Use 'Close/Last' instead of 'Close'."
