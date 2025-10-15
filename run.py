#!/usr/bin/env python3
"""
Financial Report Extractor - Command Line Interface

A simple CLI script to run the Financial Report Extractor.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from financial_extractor.main import main

if __name__ == "__main__":
    main()
