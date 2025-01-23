#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

from __future__ import print_function

__author__ = "First Last"
__copyright__ = "Copyright 2018, First Last"
__credits__ = ["C D", "A B"]
__license__ = "Apache 2.0"
__version__ = "1.0.1"
__maintainer__ = "First Last"
__email__ = "test@example.org"
__status__ = "Development"

import pandas as pd

def read_excel_with_tabs(file_path):
    """
    Reads an Excel spreadsheet with multiple tabs and returns a dictionary of DataFrames.

    Parameters:
        file_path (str): The path to the Excel file.

    Returns:
        dict: A dictionary where the keys are sheet names and the values are DataFrames.
    """
    try:
        # Use pandas to read the Excel file with all sheets
        sheets = pd.read_excel(file_path, sheet_name=None)
        return sheets
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return None

# Example usage:
# file_path = 'your_excel_file.xlsx'
# data = read_excel_with_tabs(file_path)
# for sheet_name, df in data.items():
#     print(f"Sheet: {sheet_name}")
#     print(df.head())
