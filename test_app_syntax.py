#!/usr/bin/env python3
"""Test script to verify app.py syntax and logic."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

print("Testing app.py syntax and imports...")

try:
    # Test that the file can be parsed
    with open('app.py', 'r') as f:
        code = f.read()
        compile(code, 'app.py', 'exec')
    print("✅ app.py syntax is valid")
    
    # Test basic imports work
    import streamlit as st
    from src.graph.workflow import graph, get_config
    import config
    print("✅ All imports successful")
    
    # Test that required modules exist
    from src.tools import (
        wikipedia_tool,
        stock_data_tool,
        calculate_returns_tool,
    )
    print("✅ All tools import successfully")
    
    print("\n✅ All checks passed! App should be ready to run.")
    print("\nTo start the app, run:")
    print("  streamlit run app.py")
    
except SyntaxError as e:
    print(f"❌ Syntax error in app.py: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
