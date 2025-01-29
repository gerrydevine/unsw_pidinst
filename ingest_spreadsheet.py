#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

# from __future__ import print_function

__author__ = "Gerry Devine"

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
    

def handle_owner(owner_id):
    owner = owners_df.loc[owners_df['ID'] == owner_id]
    # Owner Name
    print('')
    print(f"Owner Name = {owner['Owner_Name'].values[0]}")
    # Owner Contact
    print('')
    print(f"Owner Contact = {owner['Owner_Contact'].values[0]}")
    # Owner Type
    print('')
    print(f"Owner Type = {owner['Owner_Type'].values[0]}")
    # Owner Identifier Value
    print('')
    print(f"Owner Identifier Value = {owner['Owner_Identifier_Value'].values[0]}")
    # Owner Identifier Type
    print('')
    print(f"Owner Identifier Type = {owner['Owner_Identifier_Type'].values[0]}")


def handle_manufacturer(manufacturer_id):
    manufacturer = manufacturers_df.loc[manufacturers_df['ID'] == manufacturer_id]
    # Manufacturer Name
    print('')
    print(f"Manufacturer Name = {manufacturer['Manufacturer_Name'].values[0]}")
    # Manufacturer Name Type
    print('')
    print(f"Manufacturer Name Type = {manufacturer['Manufacturer_Name_Type'].values[0]}")
    # Manufacturer Identifier Value
    print('')
    print(f"Manufacturer Identifier Value = {manufacturer['Manufacturer_Identifier_Value'].values[0]}")
    # Manufacturer Identifier Type
    print('')
    print(f"Manufacturer Identifier Type = {manufacturer['Manufacturer_Identifier_Type'].values[0]}")


def handle_model(model_id):
    model = model_df.loc[model_df['ID'] == model_id]
    # Model Name
    print('')
    print(f"Model Name = {model['Model_Name'].values[0]}")
    # Model Identifier Value
    print('')
    print(f"Model Identifier Value = {model['Model_Identifier_Value'].values[0]}")
    # Model Identifier Type
    print('')
    print(f"Model Identifier Type = {model['Model_Identifier_Type'].values[0]}")


def handle_instrument_type(instrument_type_id):
    instrument_type = instrument_types_df.loc[instrument_types_df['ID'] == instrument_type_id]
    # Instrument_type Name
    print('')
    print(f"Instrument Type Name = {instrument_type['Instrument_Type_Name'].values[0]}")
    # Instrument Type Identifier Value
    print('')
    print(f"Instrument Type Identifier Value = {instrument_type['Instrument_Type_Identifier_Value'].values[0]}")
    # Instrument Type Identifier Type
    print('')
    print(f"Instrument Type Identifier Type = {instrument_type['Instrument_Type_Identifier_Type'].values[0]}")


def handle_related_identifier(related_identifier_id):
    related_identifier = related_identifiers_df.loc[related_identifiers_df['ID'] == related_identifier_id]
    # Related Identifier Value
    print('')
    print(f"Related Identifier Value = {related_identifier['Related_Identifier_Value'].values[0]}")
    # Related Identifier Type
    print('')
    print(f"Related Identifier Type = {related_identifier['Related_Identifier_Type'].values[0]}")
    # Related Identifier Relation Type
    print('')
    print(f"Related Identifier Relation Type = {related_identifier['Related_Identifier_Relation_Type'].values[0]}")
    # Related Identifier Name
    print('')
    print(f"Related Identifier Name = {related_identifier['Related_Identifier_Name'].values[0]}")


def handle_alternate_identifier(alternate_identifier_id):
    alternate_identifier = alternate_identifiers_df.loc[alternate_identifiers_df['ID'] == alternate_identifier_id]
    # Alternate Identifier Value
    print('')
    print(f"Alternate Identifier Value = {alternate_identifier['Alternate_Identifier_Value'].values[0]}")
    # AlternateIdentifier Type
    print('')
    print(f"Alternate Identifier Type = {alternate_identifier['Alternate_Identifier_Type'].values[0]}")


# READ IN SPREADSHEET
file_path = 'Instrument_Batch_1.xlsx'
data = read_excel_with_tabs(file_path)
for sheet_name, df in data.items():
    globals()[f"{sheet_name.replace(" ", "_").lower()}_df"] = df

# Loop through main instruments dataframe
for index, row in instruments_df.iterrows():
    # Instrument Name
    print('')
    print(f"Instrument Name = {row['Name']}")

    # Instrument Description
    print('')
    print(f"Instrument Description = {row['Description']}")

    # Instrument Owners
    if isinstance(row['Owners'], str):
        owner_ids = row['Owners'].split('|')
    else:
        owner_ids = list(str(row['Owners']))
    for owner_id in owner_ids:
        handle_owner(int(owner_id))

    # Instrument Manufacturers
    if isinstance(row['Manufacturers'], str):
        manufacturer_ids = row['Manufacturers'].split('|')
    else:
        manufacturer_ids = list(str(row['Manufacturers']))
    for manufacturer_id in manufacturer_ids:
        handle_manufacturer(int(manufacturer_id))

    # Instrument Model
    model_id = row['Model']
    handle_model(int(model_id))

    # Instrument Types
    if isinstance(row['Instrument_Types'], str):
        instrument_type_ids = row['Instrument_Types'].split('|')
    else:
        instrument_type_ids = list(str(row['Instrument_Types']))
    for instrument_type_id in instrument_type_ids:
        handle_instrument_type(int(instrument_type_id))

    # Related Identifiers
    if isinstance(row['Related_Identifiers'], str):
        related_identifier_ids = row['Related_Identifiers'].split('|')
    else:
        related_identifier_ids = list(str(row['Related_Identifiers']))
    for related_identifier_id in related_identifier_ids:
        handle_related_identifier(int(related_identifier_id))

    # Alternate Identifiers
    if isinstance(row['Alternate_Identifiers'], str):
        alternate_identifier_ids = row['Alternate_Identifiers'].split('|')
    else:
        alternate_identifier_ids = list(str(row['Alternate_Identifiers']))
    for alternate_identifier_id in alternate_identifier_ids:
        handle_alternate_identifier(int(alternate_identifier_id))


print('Done')
    
