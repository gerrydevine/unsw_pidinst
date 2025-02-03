#!/usr/bin/env python3

""" Ingest instrument information from a nominated ROS record and allocate PIDInst DOI 
"""

__author__ = "Gerry Devine"


import pandas as pd
from ros_utils import ros_login, get_ros_record_by_id
from unsw_pidinst.instrument import Identifier, Instrument, Owner, OwnerIdentifier, Manufacturer, ManufacturerIdentifier, \
    Model, ModelIdentifier, RelatedIdentifier, InstrumentType, InstrumentTypeIdentifier, AlternateIdentifier, Date 


ROS_EQUIPMENT_ID = 'E35F45EF-4ADC-453F-8F20-EB85B714FD63'


def handle_creators(instrument_creators, token):
    if isinstance(instrument_creators, dict):
        newlist = []
        newlist.append(instrument_creators)
        instrument_creators = newlist

    creators = []
    for creator in instrument_creators:
        c = {}

        c["name"] = f"{creator['api:people']['api:person']['api:last-name']}, {creator['api:people']['api:person']['api:first-names']}"
        c["givenName"] = f"{creator['api:people']['api:person']['api:first-names']}"
        c["familyName"] = f"{creator['api:people']['api:person']['api:last-name']}"
        c["nameType"] = "Personal"

        # Get ORCID, if existing
        if creator['api:people']['api:person'].get('api:links'):
            link_url = creator['api:people']['api:person']['api:links']['api:link']['@href']
            headers = {'Authorization': token}
            response = requests.request("GET", link_url, headers=headers)
            time.sleep(1)
            data = xmltodict.parse(response.content)
            identifiers = data['api:response']['api:result']['api:object']['api:user-identifier-associations']['api:user-identifier-association']
            orcid_entry = next((i for i in identifiers if i['@scheme'] == "orcid"), None)

            if orcid_entry:
                c['nameIdentifiers'] = []
                c['nameIdentifiers'].append(
                    	{
							"nameIdentifier": f"https://orcid.org/{orcid_entry['#text']}",
							"nameIdentifierScheme": "ORCID",
							"schemeUri": "https://orcid.org"
						}
                )

        # Add Affiliation
        c["affiliation"] = [
            {
              "affiliationIdentifier": "https://ror.org/03r8z3t63",
              "affiliationIdentifierScheme": "ROR",
              "name": "UNSW Sydney",
              "schemeUri": "https://ror.org/"
            }
        ]

        creators.append(c)

    return creators


    

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


def generate_pidinst(instrument_individual_record):
    ''' Generate a PIDINST record from ros information '''

    # GET INSTRUMENT NAME/TITLE AND INSTANTIATE NEW INSTRUMENT MODEL
    instrument_name = next((i for i in instrument_individual_record['api:native']['api:field'] if i['@name'] == "name"), None)
    assert instrument_name is not None, 'Instrument name cannot be None'
    instrument_1 = Instrument(name=instrument_name['api:text'])

    # SET INSTRUMENT OWNER/CONTRIBUTOR (HOSTING INSTITUTION)

    # instrument_creators = next((i for i in instrument_individual_record['api:native']['api:field'] if i['@name'] == "contacts"), None)
    hosting_instititution_name = next((i for i in instrument_individual_record['api:native']['api:field'] if i['@name'] == "contacts"), None)
    if instrument_creators:
        creators = handle_creators(instrument_creators, ros_token)
        attrs["creators"] = creators
    else:
        print(f"Instrument Contacts = None")

    # SET DESCRIPTION
    instrument_description = next((i for i in instrument_individual_record['api:native']['api:field'] if i['@name'] == "description"), None)
    if instrument_description:
        print(f"Instrument Description = {instrument_description['api:text']}")

    attrs["descriptions"] = []
    attrs["descriptions"].append(
        {
            "lang": "en-US",
            "description": instrument_description['api:text'],
            "descriptionType": "Abstract"
        }
    )








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


def get_ros_instrument_info(ros_intrument_id, ros_token):
    ''' Retrieve information about an instrument in ROS '''

    # GET ROS RECORD BY ID
    record_info = get_ros_record_by_id(ros_intrument_id, ros_token)
    ros_instrument_info = record_info['api:response']['api:result']['api:object']

    # GET INDIVIDUAL INSTRUMENT MANUAL SOURCE RECORD
    assert isinstance(ros_instrument_info['api:records']['api:record'], dict), 'Error: Multiple sources found!'
    assert ros_instrument_info['api:records']['api:record']['@source-name'] == 'manual', "Source is not of type 'Manual'"

    instrument_individual_record = ros_instrument_info['api:records']['api:record']

    return instrument_individual_record


def main():
        
    # LOG IN TO ROS
    ros_token = ros_login()

    # PULL INFO FROM ROS INSTRUMENT RECORD
    ros_instrument_info = get_ros_instrument_info(ROS_EQUIPMENT_ID, ros_token)

    # GENERATE PIDINST RECORD AND LANDING PAGE
    generate_pidinst(ros_instrument_info)



    print('Done!')



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
    
