#!/usr/bin/env python3
"""Test runner for all EXASPERATION tests."""

import os
import sys
import unittest
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

def run_tests(pattern="test_*.py", verbose=False):
    """Run all tests matching the pattern.
    
    Args:
        pattern: Test filename pattern to match
        verbose: Whether to use verbose output
        
    Returns:
        Number of test failures
    """
    loader = unittest.TestLoader()
    
    # Discover all tests in the project
    test_suites = [
        loader.discover(str(project_root / "src"), pattern=pattern),
        loader.discover(str(project_root / "tests"), pattern=pattern)
    ]
    
    # Combine all test suites
    all_tests = unittest.TestSuite(test_suites)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
    result = runner.run(all_tests)
    
    return len(result.failures) + len(result.errors)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run EXASPERATION tests")
    parser.add_argument("--pattern", default="test_*.py", help="Test filename pattern")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()
    
    print(f"Running tests matching pattern: {args.pattern}")
    failures = run_tests(args.pattern, args.verbose)
    
    sys.exit(failures)