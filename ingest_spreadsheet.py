#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

# from __future__ import print_function

__author__ = "Gerry Devine"

import pandas as pd
from unsw_pidinst.instrument import Identifier, Instrument, Owner, OwnerIdentifier, Manufacturer, ManufacturerIdentifier, \
    Model, ModelIdentifier, RelatedIdentifier, InstrumentType, InstrumentTypeIdentifier, AlternateIdentifier, Date 


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

    owner_1 = Owner(owner_name=owner['Owner_Name'].values[0], owner_contact=owner['Owner_Contact'].values[0], owner_type=owner['Owner_Type'].values[0])
    owner_identifier_1 = OwnerIdentifier(owner_identifier_value=owner['Owner_Identifier_Value'].values[0], owner_identifier_type=owner['Owner_Identifier_Type'].values[0]) 
    owner_1.owner_identifier = owner_identifier_1

    return owner_1


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

    manufacturer_1 = Manufacturer(manufacturer_name=manufacturer['Manufacturer_Name'].values[0], manufacturer_name_type=manufacturer['Manufacturer_Name_Type'].values[0])
    manufacturer_identifier_1 = ManufacturerIdentifier(manufacturer_identifier_value=manufacturer['Manufacturer_Identifier_Value'].values[0], manufacturer_identifier_type=manufacturer['Manufacturer_Identifier_Type'].values[0]) 
    manufacturer_1.manufacturer_identifier = manufacturer_identifier_1

    return manufacturer_1


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

    model_1 = Model(model_name=model['Model_Name'].values[0])
    model_identifier_1 = ModelIdentifier(model_identifier_value=model['Model_Identifier_Value'].values[0], model_identifier_type=model['Model_Identifier_Type'].values[0]) 
    model_1.model_identifier = model_identifier_1

    return model_1


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

    instrument_type_1 = InstrumentType(instrument_type_name=instrument_type['Instrument_Type_Name'].values[0])
    instrument_type_identifier_1 = InstrumentTypeIdentifier(instrument_type_identifier_value=instrument_type['Instrument_Type_Identifier_Value'].values[0], instrument_type_identifier_type=instrument_type['Instrument_Type_Identifier_Type'].values[0]) 
    instrument_type_1.instrument_type_identifier = instrument_type_identifier_1

    return instrument_type_1


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

    related_identifier_1 = RelatedIdentifier(related_identifier_value=related_identifier['Related_Identifier_Value'].values[0], related_identifier_type=related_identifier['Related_Identifier_Type'].values[0], related_identifier_relation_type=related_identifier['Related_Identifier_Relation_Type'].values[0], related_identifier_name=related_identifier['Related_Identifier_Name'].values[0])
    return related_identifier_1


def handle_alternate_identifier(alternate_identifier_id):
    alternate_identifier = alternate_identifiers_df.loc[alternate_identifiers_df['ID'] == alternate_identifier_id]
    # Alternate Identifier Value
    print('')
    print(f"Alternate Identifier Value = {alternate_identifier['Alternate_Identifier_Value'].values[0]}")
    # AlternateIdentifier Type
    print('')
    print(f"Alternate Identifier Type = {alternate_identifier['Alternate_Identifier_Type'].values[0]}")

    alternate_identifier_1 = AlternateIdentifier(alternate_identifier_value=alternate_identifier['Alternate_Identifier_Value'].values[0], alternate_identifier_type=alternate_identifier['Alternate_Identifier_Type'].values[0])
    return alternate_identifier_1


def handle_date(date_id):
    date = dates_df.loc[dates_df['ID'] == date_id]
    # Date Value
    print('')
    print(f"Date Value = {pd.to_datetime(str(date['Date_Value'].values[0])).strftime('%Y-%m-%d')}")
    # Date Type
    print('')
    print(f"Date Type = {date['Date_Type'].values[0]}")

    date_1 = Date(date_value=date['Date_Value'].values[0], date_type=date['Date_Type'].values[0])
    return date_1


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
    instrument_1 = Instrument(name=row['Name'])

    # Instrument Description
    print('')
    print(f"Instrument Description = {row['Description']}")
    instrument_1.description = row['Description']

    # Instrument Owners
    if isinstance(row['Owners'], str):
        owner_ids = row['Owners'].split('|')
    else:
        owner_ids = list(str(row['Owners']))
    for owner_id in owner_ids:
        owner_details = handle_owner(int(owner_id))
        instrument_1.append_owner(owner_details)

    # Instrument Manufacturers
    if isinstance(row['Manufacturers'], str):
        manufacturer_ids = row['Manufacturers'].split('|')
    else:
        manufacturer_ids = list(str(row['Manufacturers']))
    for manufacturer_id in manufacturer_ids:
        manufacturer_details = handle_manufacturer(int(manufacturer_id))
        instrument_1.append_manufacturer(manufacturer_details)

    # Instrument Model
    model_id = row['Model']
    model_details = handle_model(int(model_id))
    instrument_1.model = model_details

    # Instrument Types
    if isinstance(row['Instrument_Types'], str):
        instrument_type_ids = row['Instrument_Types'].split('|')
    else:
        instrument_type_ids = list(str(row['Instrument_Types']))
    for instrument_type_id in instrument_type_ids:
        instrument_type_details = handle_instrument_type(int(instrument_type_id))
        instrument_1.append_instrument_type(instrument_type_details)

    # Related Identifiers
    if isinstance(row['Related_Identifiers'], str):
        related_identifier_ids = row['Related_Identifiers'].split('|')
    else:
        related_identifier_ids = list(str(row['Related_Identifiers']))
    for related_identifier_id in related_identifier_ids:
        related_identifier_details = handle_related_identifier(int(related_identifier_id))
        instrument_1.append_related_identifier(related_identifier_details)

    # Alternate Identifiers
    if isinstance(row['Alternate_Identifiers'], str):
        alternate_identifier_ids = row['Alternate_Identifiers'].split('|')
    else:
        alternate_identifier_ids = list(str(row['Alternate_Identifiers']))
    for alternate_identifier_id in alternate_identifier_ids:
        alternate_identifier_details = handle_alternate_identifier(int(alternate_identifier_id))
        instrument_1.append_alternate_identifier(alternate_identifier_details)

    # Dates
    if isinstance(row['Dates'], str):
        date_ids = row['Dates'].split('|')
    else:
        date_ids = list(str(row['Dates']))
    for date_id in date_ids:
        date_details = handle_date(int(date_id))
        instrument_1.append_date(date_details)

    # Generate an initial landing page (without DOI) 
    instrument_1.landing_page = f"https://gerrydevine.github.io/instrument-catalogue/instruments/{instrument_1.local_id}"
    instrument_1.generate_webpage()

    # Allocate a doi
    instrument_1.allocate_doi()

    # Update landing page (with DOI) 
    instrument_1.landing_page = f"https://gerrydevine.github.io/instrument-catalogue/instruments/{instrument_1.local_id}"
    instrument_1.generate_webpage(use_github=True)

print('Done')
    
