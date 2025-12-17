"""Main test runner for FinGPT test suite."""

import sys
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_all_tests():
    """Run all tests with detailed output."""
    print("=" * 70)
    print("🧪 FinGPT Test Suite")
    print("=" * 70)
    
    test_files = [
        "tests/test_analysis_tools.py",
        "tests/test_data_tools.py",
        "tests/test_visualization_tools.py",
        "tests/test_wikipedia_tool.py",
        "tests/test_workflow.py",
        "tests/test_e2e.py",
        "tests/test_tools.py",
        "tests/test_agents.py",
        "tests/test_graph.py",
        "smoke_test.py"
    ]
    
    # Run pytest with verbose output
    args = [
        "-v",  # Verbose
        "--tb=short",  # Shorter traceback format
        "--color=yes",  # Colored output
        "-ra",  # Show summary of all test outcomes
        *test_files
    ]
    
    exit_code = pytest.main(args)
    
    print("\n" + "=" * 70)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed. See output above.")
    print("=" * 70)
    
    return exit_code


def run_quick_tests():
    """Run a subset of quick tests."""
    print("🚀 Running quick tests...")
    
    args = [
        "-v",
        "--tb=short",
        "-k", "test_valid or test_available",  # Only run specific test patterns
        "tests/"
    ]
    
    return pytest.main(args)


def run_integration_tests():
    """Run integration tests only."""
    print("🔗 Running integration tests...")
    
    args = [
        "-v",
        "--tb=short",
        "tests/test_workflow.py"
    ]
    
    return pytest.main(args)


def run_tool_tests():
    """Run tool tests only."""
    print("🔧 Running tool tests...")
    
    args = [
        "-v",
        "--tb=short",
        "tests/test_analysis_tools.py",
        "tests/test_data_tools.py",
        "tests/test_visualization_tools.py",
        "tests/test_wikipedia_tool.py"
    ]
    
    return pytest.main(args)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="FinGPT Test Runner")
    parser.add_argument(
        "--mode",
        choices=["all", "quick", "integration", "tools"],
        default="all",
        help="Test mode to run"
    )
    
    args = parser.parse_args()
    
    if args.mode == "all":
        exit_code = run_all_tests()
    elif args.mode == "quick":
        exit_code = run_quick_tests()
    elif args.mode == "integration":
        exit_code = run_integration_tests()
    elif args.mode == "tools":
        exit_code = run_tool_tests()
    
    sys.exit(exit_code)
