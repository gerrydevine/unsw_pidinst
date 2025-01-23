import os
import datetime
from dotenv import load_dotenv
from base64 import b64encode
from .config import DOI_PREFIX

load_dotenv()


def datacite_login():
    ''' Login to DATACITE
    - Returns a Basic Auth Token 

    '''
    datacite_username = os.environ.get('DATACITE_USERNAME')
    datacite_password = os.environ.get('DATACITE_PASSWORD')
    datacite_token = b64encode(f"{datacite_username.upper()}:{datacite_password}".encode('utf-8')).decode("ascii")

    return f"Basic {datacite_token}"


def generate_datacite_payload(pidinst_metadata):
    ''' Map PIDInst metadata to a Datacite-friendly payload '''

    # Create new skeleton object to store instrument payload
    payload = {}
    payload["data"] = {}
    payload["data"]["type"] = 'dois'
    
    # Create empty Attributes dictionary then populate
    attrs = {}

    # SET DOI PREFIX
    attrs["prefix"] = DOI_PREFIX

    # SET PUBLISHER (DEFAULTING TO UNSW)
    attrs["publisher"] = {
        "name": "UNSW Sydney",
        "publisherIdentifier":"https://ror.org/03r8z3t63",
        "publisherIdentifierScheme":"ROR",
        "schemeUri": "https://ror.org/"
    },
    
    # SET PUBLICATION YEAR
    attrs["publicationYear"] = datetime.date.today().year

    # SET RESOURCE TYPE
    attrs["types"] = {"resourceTypeGeneral": "Instrument"}

    # SET INSTRUMENT NAME/TITLE (PIDINST NAME TO DATACITE TITLE)
    attrs["titles"] = [
        {
            "title": pidinst_metadata.name,
            "titleType": 'Other'
        }
    ]

    # SET URL/LANDING PAGE
    attrs["url"] = pidinst_metadata.landing_page

    # SET INSTRUMENT DESCRIPTION (DESCRIPTIONTYPE: ABSTRACT)
    attrs['descriptions'] = []
    if pidinst_metadata.description:
        attrs["descriptions"].append(
            {
                "lang": "en-US",
                "description": pidinst_metadata.description,
                "descriptionType": "Abstract"
            }
        )

    # POPULATE DATACITE CONTRIBUTORS (PIDINST OWNER TO DATACITE CONTRIBUTOR)
    contributors = []
    for owner in pidinst_metadata.owners:
        c = {}

        # Name
        c["name"] = owner.owner_name

        # Name Type
        if owner.owner_type == "HostingInstitution":
            c["nameType"] = "Organizational"
        else:
            c["nameType"] = "Personal"

        # Contributor Type
        c["contributorType"] = owner.owner_type

        # Get ORCID, if existing
        if hasattr(owner, 'owner_identifier'):
            if owner.owner_identifier.owner_identifier_type == 'ORCID':
                c['nameIdentifiers'] = [
                    	{
							"nameIdentifier": f"https://orcid.org/{owner.owner_identifier.owner_identifier_value}",
							"nameIdentifierScheme": "ORCID",
							"schemeUri": "https://orcid.org"
						}
                ]
            elif owner.owner_identifier.owner_identifier_type == 'ROR':
                c['nameIdentifiers'] = [
                    	{
							"nameIdentifier": f"https://ror.org/{owner.owner_identifier.owner_identifier_value}",
							"nameIdentifierScheme": "ROR",
							"schemeUri": "https://ror.org"
						}
                ]

        # Add Affiliations if not an institution (assumed UNSW)
        affils = []
        if owner.owner_type != "HostingInstitution":
            affils.append( 
                {
                    "affiliationIdentifier": "https://ror.org/03r8z3t63",
                    "affiliationIdentifierScheme": "ROR",
                    "name": "UNSW Sydney",
                    "schemeUri": "https://ror.org/"
                }
            )
        c["affiliation"] = affils

        contributors.append(c)

    attrs["contributors"] = contributors


    # POPULATE DATACITE CREATORS (PIDINST MANUFACTURER TO DATACITE CREATOR)
    creators = []
    for manufacturer in pidinst_metadata.manufacturers:
        c = {}

        # Name
        c["name"] = manufacturer.manufacturer_name

        # Name Type
        c["nameType"] = manufacturer.manufacturer_name_type

        # Get ORCID, if existing
        if hasattr(manufacturer, 'manufacturer_identifier'):
            if manufacturer.manufacturer_identifier.manufacturer_identifier_type == 'ORCID':
                c['nameIdentifiers'] = [
                    	{
							"nameIdentifier": f"https://orcid.org/{manufacturer.manufacturer_identifier.manufacturer_identifier_value}",
							"nameIdentifierScheme": "ORCID",
							"schemeUri": "https://orcid.org"
						}
                ]
            elif manufacturer.manufacturer_identifier.manufacturer_identifier_type == 'ROR':
                c['nameIdentifiers'] = [
                    	{
							"nameIdentifier": f"https://ror.org/{manufacturer.manufacturer_identifier.manufacturer_identifier_value}",
							"nameIdentifierScheme": "ROR",
							"schemeUri": "https://ror.org"
						}
                ]
            elif manufacturer.manufacturer_identifier.manufacturer_identifier_type == 'URL':
                c['nameIdentifiers'] = [
                    	{
							"nameIdentifier": manufacturer.manufacturer_identifier.manufacturer_identifier_value,
							"nameIdentifierScheme": "URL",
						}
                ]

        # Add Affiliations if not an institution (assumed UNSW)
        affils = []
        if manufacturer.manufacturer_name_type != "Organizational":
            affils.append( 
                {
                    "affiliationIdentifier": "https://ror.org/03r8z3t63",
                    "affiliationIdentifierScheme": "ROR",
                    "name": "UNSW Sydney",
                    "schemeUri": "https://ror.org/"
                }
            )
        c["affiliation"] = affils

        creators.append(c)

    attrs["creators"] = creators


    # SET INSTRUMENT MODEL (DESCRIPTIONTYPE: TECHNICALINFO)
    if pidinst_metadata.model:
        attrs["descriptions"].append(
            {
                "lang": "en-US",
                "description": pidinst_metadata.model.model_name,
                "descriptionType": "TechnicalInfo"
            }
        )


    # POPULATE RELATED IDENTIFIERS
    related_identifiers = []
    for related_identifier in pidinst_metadata.related_identifiers:
        c = {}

        # Relation Type
        c["relationType"] = related_identifier.related_identifier_relation_type

        # related identifier Identifier
        c["relatedIdentifier"] = related_identifier.related_identifier_value

        # related identifier type
        c["relatedIdentifierType"] = related_identifier.related_identifier_type

        related_identifiers.append(c)

    attrs["relatedIdentifiers"] = related_identifiers


    # POPULATE ALTERNATE IDENTIFIERS
    alternate_identifiers = []
    for alternate_identifier in pidinst_metadata.alternate_identifiers:
        c = {}

        # Value
        c["alternateIdentifier"] = alternate_identifier.alternate_identifier_value
        # Alternate identifier type
        c["alternateIdentifierType"] = alternate_identifier.alternate_identifier_type

        alternate_identifiers.append(c)

    attrs["alternateIdentifiers"] = alternate_identifiers


    # POPULATE DATES
    dates = []
    for date in pidinst_metadata.dates:
        c = {}

        # Value
        c["date"] = date.date_value
        # Date type
        c["dateType"] = "Other"
        # Date Information
        c["dateInformation"] = date.date_type

        dates.append(c)

    attrs["dates"] = dates


    payload["data"]["attributes"] = attrs

    return payload
