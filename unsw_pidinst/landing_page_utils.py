import datetime
import os
from github import Github
from .config import GIT_BRANCH, GITHUB_REPO
from dotenv import load_dotenv

load_dotenv()


DOI_LOGO = '''
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 130 130">
        <circle style="fill:#fcb425" cx="65" cy="65" r="64"/>
        <path style="fill:#231f20" d="m 49.819127,84.559148 -11.854304,0 0,-4.825665 c -1.203594,1.510894 -4.035515,3.051053 -5.264716,3.742483 -2.151101,1.203585 -5.072066,1.987225 -7.812161,1.987225 -4.430246,0 -8.373925,-1.399539 -11.831057,-4.446924 -4.1229464,-3.636389 -6.0602455,-9.19576 -6.0602455,-15.188113 0,-6.094791 2.1126913,-10.960381 6.3380645,-14.59676 3.354695,-2.893745 7.457089,-5.209795 11.810505,-5.209795 2.535231,0 5.661807,0.227363 7.889738,1.302913 1.280414,0.614601 3.572628,2.060721 4.929872,3.469179 l 0,-25.420177 11.854304,0 z m -12.1199,-18.692584 c 0,-2.253538 -0.618258,-4.951555 -2.205973,-6.513663 -1.587724,-1.587724 -4.474153,-2.996182 -6.727691,-2.996182 -2.509615,0 -4.834476,1.825511 -6.447807,3.720535 -1.306031,1.536501 -1.959041,3.905269 -1.959041,5.877114 0,1.971835 0.740815,4.165004 2.046836,5.701505 1.587714,1.895025 3.297985,3.193739 5.833216,3.193739 2.279145,0 4.989965,-0.956662 6.552083,-2.51877 1.587714,-1.562108 2.908377,-4.185134 2.908377,-6.464278 z"/>
        <path style="fill:#fff" d="m 105.42764,25.617918 c -1.97184,0 -3.64919,0.69142 -5.03204,2.074271 -1.357247,1.357245 -2.035864,3.021779 -2.035864,4.993633 0,1.971835 0.678617,3.649193 2.035864,5.032034 1.38285,1.382861 3.0602,2.074281 5.03204,2.074281 1.99744,0 3.67479,-0.678627 5.03203,-2.035861 1.38285,-1.382861 2.07428,-3.073012 2.07428,-5.070454 0,-1.971854 -0.69143,-3.636388 -2.07428,-4.993633 -1.38285,-1.382851 -3.0602,-2.074271 -5.03203,-2.074271 z M 74.219383,45.507921 c -7.323992,0 -12.970625,2.283009 -16.939921,6.848949 -3.277876,3.782438 -4.916803,8.118252 -4.916803,13.008406 0,5.430481 1.626124,10.009834 4.878383,13.738236 3.943689,4.538918 9.475093,6.808622 16.59421,6.808622 7.093512,0 12.612122,-2.269704 16.555801,-6.808622 3.252259,-3.728402 4.878393,-8.1993 4.878393,-13.413648 0,-5.160323 -1.638938,-9.604602 -4.916803,-13.332994 -4.020509,-4.56594 -9.398263,-6.848949 -16.13326,-6.848949 z m 24.908603,1.386686 0,37.634676 12.599304,0 0,-37.634676 -12.599304,0 z M 73.835252,56.975981 c 2.304752,0 4.263793,0.852337 5.877124,2.554426 1.638928,1.675076 2.458402,3.727881 2.458402,6.159457 0,2.458578 -0.806671,4.538022 -2.419992,6.240111 -1.613331,1.675086 -3.585175,2.514099 -5.915534,2.514099 -2.612051,0 -4.737546,-1.027366 -6.376474,-3.080682 -1.331637,-1.648053 -1.997451,-3.539154 -1.997451,-5.673528 0,-2.107362 0.665814,-3.985138 1.997451,-5.633201 1.638928,-2.053316 3.764423,-3.080682 6.376474,-3.080682 z"/>
    </svg>
'''
ORCID_LOGO = '''
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Layer_1" x="0px" y="0px" viewBox="0 0 256 256" style="enable-background:new 0 0 256 256;" width="20" height="20">
        <style type="text/css">
            .st0{fill:#A6CE39;}
            .st1{fill:#FFFFFF;}
        </style>
        <path class="st0" d="M256,128c0,70.7-57.3,128-128,128C57.3,256,0,198.7,0,128C0,57.3,57.3,0,128,0C198.7,0,256,57.3,256,128z"/>
        <g>
            <path class="st1" d="M86.3,186.2H70.9V79.1h15.4v48.4V186.2z"/>
            <path class="st1" d="M108.9,79.1h41.6c39.6,0,57,28.3,57,53.6c0,27.5-21.5,53.6-56.8,53.6h-41.8V79.1z M124.3,172.4h24.5   c34.9,0,42.9-26.5,42.9-39.7c0-21.5-13.7-39.7-43.7-39.7h-23.7V172.4z"/>
            <path class="st1" d="M88.7,56.8c0,5.5-4.5,10.1-10.1,10.1c-5.6,0-10.1-4.6-10.1-10.1c0-5.6,4.5-10.1,10.1-10.1   C84.2,46.7,88.7,51.3,88.7,56.8z"/>
        </g>
    </svg>
'''


def get_owners_html(owners):
    ''' Return a html blurb of owner details '''
    
    html = ''
    for owner in owners:
        # Use orcid linked name if applicable
        try:
            if owner.owner_identifier.owner_identifier_type == 'ORCID' and owner.owner_identifier.owner_identifier_value:
                orcid = owner.owner_identifier.owner_identifier_value
                name = owner.owner_name
                owner_html = f"<p><a href='https://orcid.org/{orcid}'>{name} {ORCID_LOGO}</a></p>"
            else:
                name = owner.owner_name
                owner_html = f"<p>{name}</p>"

        except (NameError, AttributeError):
            name = owner.owner_name
            owner_html = f"<p>{name}</p>"

        html += owner_html

    return html


def get_manufacturers_html(manufacturers):
    ''' Return a html blurb of manufacturer details '''
    
    html = ''
    for manufacturer in manufacturers:
        try:
            if manufacturer.manufacturer_identifier.manufacturer_identifier_type == 'URL' and manufacturer.manufacturer_identifier.manufacturer_identifier_value:
                url = manufacturer.manufacturer_identifier.manufacturer_identifier_value
                name = manufacturer.manufacturer_name
                manufacturer_html = f"<p><a href='{url}'>{name}</a></p>"
            else:
                name = manufacturer.manufacturer_name
                manufacturer_html = f"<p>{name}</p>"

        except (NameError, AttributeError):
            name = manufacturer.manufacturer_name
            manufacturer_html = f"<p>{name}</p>"

        html += manufacturer_html

    return html


def get_model_html(model):
    ''' Return a html blurb of model details '''
    
    try:
        if model.model_identifier.model_identifier_type == 'URL' and model.model_identifier.model_identifier_value:
            url = model.model_identifier.model_identifier_value
            name = model.model_name
            html = f"<p><a href='{url}'>{name}</a></p>"
        else:
            name = model.model_name
            html = f"<p>{name}</p>"

    except (NameError, AttributeError):
        name = model.model_name
        html = f"<p>{name}</p>"

    return html


def get_related_identifiers_html(related_identifiers):
    ''' Return a html blurb of related identifiers details '''
    
    html = ''
    for related_identifier in related_identifiers:
        # Use DOI link if applicable
        try:
            if related_identifier.related_identifier_type == 'DOI' and related_identifier.related_identifier_value:
                doi = related_identifier.related_identifier_value
                relation = related_identifier.related_identifier_relation_type
                related_identifier_html = f"<p>{relation}: <a href='https://doi.org/{doi}'>{doi} {DOI_LOGO}</a></p>"
            else:
                related_identifier_html = f"<p>{related_identifier.related_identifier_value}</p>"

        except (NameError, AttributeError):
            related_identifier_html = f"<p>{related_identifier.related_identifier_value}</p>"

        html += related_identifier_html

    return html


def push_to_github(name, filename):
    ''' Push webpage to github pages '''

    token = os.environ.get('GITHUB_ACCESS_TOKEN')
    g = Github(token)
    repo = g.get_user().get_repo(GITHUB_REPO)

    all_files = []
    contents = repo.get_contents("")

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

    with open(filename, 'r') as file:
        content = file.read()

    # Upload or replace on github
    if f"docs/{filename}" in all_files:
        repo_contents = repo.get_contents(f"docs/{filename}")
        repo.update_file(repo_contents.path, "committing files", content, repo_contents.sha, branch=GIT_BRANCH)
    else:
        repo.create_file(f"docs/{filename}", "committing files", content, branch=GIT_BRANCH)
        
        # Update main index 
        index_contents = repo.get_contents("docs/index.html")
        added_link = f'''
            <p><a href="{filename.split('.')[0]}">{name}</a></p>
        '''
        repo.update_file(index_contents.path, "committing files", f"{index_contents.decoded_content.decode()} {added_link}", index_contents.sha, branch=GIT_BRANCH)


def generate_webpage(instrument, use_github):
    ''' Generate a web landing page for an Instrument'''

    # OPEN TEMPLATE
    html = open("unsw_pidinst/web/templates/template1.html").read()

    # APPEND PUBLICATION DATE
    html = html.replace("__PUBLICATION_DATE__", str(datetime.date.today().year))

    # APPEND PUBLICATION DATE
    html = html.replace("__UNSW_ID__", instrument.local_id)

    # DOI
    if instrument.identifier and instrument.identifier.identifier_type == 'DOI':
        html = html.replace("__INSTRUMENT_DOI__", f"<a href='https://doi.org/{instrument.identifier.identifier_value}'>https://doi.org/{instrument.identifier.identifier_value} {DOI_LOGO}</a>")
    else:
        html = html.replace("__INSTRUMENT_DOI__", 'No DOI Allocated')

    # SET INSTRUMENT NAME/TITLE
    html = html.replace("__INSTRUMENT_NAME__", instrument.name)

    # SET DESCRIPTION
    if instrument.description:
        html = html.replace("__INSTRUMENT_DESCRIPTION__", instrument.description)
    else:
        html = html.replace("__INSTRUMENT_DESCRIPTION__", '')

    # SET INSTRUMENT OWNERS
    if hasattr(instrument, 'owners'):
        owners_html = get_owners_html(instrument.owners)
        html = html.replace("__INSTRUMENT_OWNERS__", owners_html)
    else:
        html = html.replace("__INSTRUMENT_OWNERS__", '')

    # SET INSTRUMENT MANUFACTURERS
    if hasattr(instrument, 'manufacturers'):
        manufacturers_html = get_manufacturers_html(instrument.manufacturers)
        html = html.replace("__INSTRUMENT_MANUFACTURERS__", manufacturers_html)
    else:
        html = html.replace("__INSTRUMENT_MANUFACTURERS__", '')

    # SET INSTRUMENT MODEL
    if hasattr(instrument, 'model'):
        model_html = get_model_html(instrument.model)
        html = html.replace("__INSTRUMENT_MODEL__", model_html)
    else:
        html = html.replace("__INSTRUMENT_MODEL__", '')

    # SET RELATED IDENTIFIERS
    if hasattr(instrument, 'related_identifiers'):
        related_identifiers_html = get_related_identifiers_html(instrument.related_identifiers)
        html = html.replace("__RELATED_IDENTIFIERS__", related_identifiers_html)
    else:
        html = html.replace("__RELATED_IDENTIFIERS__", '')  

    # # Instrument Inventory Number
    # instrument_inventory_number = next((i for i in instrument_individual_record['api:native']['api:field'] if i['@name'] == "inventory-number"), None)
    # if instrument_inventory_number:
    #     html = html.replace("__INSTRUMENT_INVENTORY_NUMBER__", instrument_inventory_number['api:text'])

    # # Instrument SubType
    # instrument_subtype = next((i for i in instrument_individual_record['api:native']['api:field'] if i['@name'] == "sub-type"), None)
    # if instrument_subtype:
    #     html = html.replace("__INSTRUMENT_SUBTYPE__", instrument_subtype['api:text'])

    # # Instrument Location/Address
    # instrument_location = next((i for i in instrument_individual_record['api:native']['api:field'] if i['@name'] == "addresses"), None)
    # if instrument_location:
    #     locations = get_location_html(instrument_location)
    #     html = html.replace("__INSTRUMENT_LOCATION__", ''.join(locations))

    # # Instrument Contact Organisation
    # instrument_contact_organisation = next((i for i in instrument_individual_record['api:native']['api:field'] if i['@name'] == "contact-organisation"), None)
    # if instrument_contact_organisation:
    #     html = html.replace("__INSTRUMENT_CONTACT_ORGANISATION__", instrument_contact_organisation['api:text'])

    # # Instrument Contact URL
    # instrument_contact_url = next((i for i in instrument_individual_record['api:native']['api:field'] if i['@name'] == "contact-url"), None)
    # if instrument_contact_url:
    #     html = html.replace("__INSTRUMENT_CONTACT_URL__", instrument_contact_url['api:text'])

    # WRITE HTML FILE
    with open(f"{instrument.local_id}.html", "w") as fp:
        fp.write(html)

    if use_github:
        push_to_github(instrument.name, f"{instrument.local_id}.html")

    