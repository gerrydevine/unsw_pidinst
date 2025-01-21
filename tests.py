import unittest
from unsw_pidinst.instrument import PIDInst, Identifier, Owner, OwnerIdentifier, Manufacturer, ManufacturerIdentifier, Model, ModelIdentifier, RelatedIdentifier, Instrument


class TestPIDInsts(unittest.TestCase):

    def test_valid_instance_with_identifier(self):
        identifier = Identifier(identifier_value="10.1000/retwebwb", identifier_type="DOI")
        pidinst = PIDInst(name="Instrument XYZ")
        pidinst.identifier = identifier
        self.assertIsInstance(pidinst, PIDInst, 'Something is wrong with class instantation')

    def test_valid_instance_without_identifier(self):
        pidinst = PIDInst(
            landing_page='https://www.landingpage.com', 
            name="Instrument XYZ",
        )
        self.assertIsInstance(pidinst, PIDInst, 'Something is wrong with class instantation')

    def test_non_identifier_object_set(self):
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        dummy_identifier = {'value':'ABC123'}
        with self.assertRaises(TypeError) as exc:
            pidinst.identifier = dummy_identifier
        self.assertEqual(str(exc.exception), "identifier must be instance of Identifier class")

    def test_non_related_identifier_object_set(self):
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        dummy_identifier = {'value':'ABC123'}
        with self.assertRaises(TypeError) as exc:
            pidinst.append_related_identifier(dummy_identifier)
        self.assertEqual(str(exc.exception), "related_identifier must be instance of RelatedIdentifier class")

    # SCHEMA VERSION TESTS
    def test_schema_version(self):
        identifier = Identifier(identifier_value="10.1000/retwebwb", identifier_type="DOI")
        pidinst = PIDInst(landing_page='https://www.landingpage.com', name="Instrument XYZ")
        pidinst.identifier = identifier
        self.assertEqual(pidinst._schema_version, 1.0, 'The schema version is incorrect')

    # LANDING PAGE TESTS
    def test_non_string_landing_page_error(self):
        with self.assertRaises(TypeError) as exc:
            PIDInst(landing_page=101, name="Instrument XYZ")
        self.assertEqual(str(exc.exception), "landing_page must be a string")

    def test_non_http_landing_page_error(self):
        with self.assertRaises(ValueError) as exc:
            PIDInst(landing_page='www.landingpage.com', name="Instrument XYZ")
        self.assertEqual(str(exc.exception), "landing_page must start with either http or https")

    # NAME TESTS
    def test_empty_name_error(self):
        with self.assertRaises(ValueError) as exc:
            PIDInst(landing_page='https://www.landingpage.com')
        self.assertEqual(str(exc.exception), "name cannot be None")

    def test_non_string_name_error(self):
        with self.assertRaises(TypeError) as exc:
            PIDInst(landing_page="https://mylandingpage.com", name=333)
        self.assertEqual(str(exc.exception), "name must be a string")

    def test_invalid_empty_string_name_error(self):
        with self.assertRaises(ValueError) as exc:
            PIDInst(landing_page="https://mylandingpage.com", name="")
        self.assertEqual(str(exc.exception), "name cannot be an empty string")

    def test_name_too_long_error(self):
        with self.assertRaises(ValueError) as exc:
            PIDInst(landing_page="https://mylandingpage.com", name="A"*201)
        self.assertEqual(str(exc.exception), "name must be less than 200 chars")

    # INSTRUMENT OWNER TESTS
    def test_valid_owner_object_set_on_init(self):
        owners = []
        owner = Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type="HostingInstitution")
        owner_identifier = OwnerIdentifier(owner_identifier_value="0000-ABCD-1234-WXYZ", owner_identifier_type='ORCID') 
        owner.owner_identifier = owner_identifier
        owners.append(owner)
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst', owners=owners)        

        self.assertIsInstance(pidinst, PIDInst, 'Something went wrong with class instantation')
        self.assertIsInstance(pidinst.owners[0], Owner, 'Something went wrong with class instantation')

    def test_invalid_non_owner_object_set_on_init(self):
        owners = []
        owner = {'owner_name':"Jane Doe", 'owner_contact':"jane.doe@email.com", 'owner_type': "HostingInstitution"} # Note no identifier set
        owners.append(owner)

        with self.assertRaises(TypeError) as exc:
            PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst', owners=owners)    
        self.assertEqual(str(exc.exception), "owners must be a list of Owner objects")    

    def test_invalid_non_owner_object_set_post_init(self):
        owners = []
        owner = {'owner_name':"Jane Doe", 'owner_contact':"jane.doe@email.com", 'owner_type':"HostingInstitution"}
        owners.append(owner)
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        self.assertIsInstance(pidinst, PIDInst, 'Something went wrong with class instantation')

        with self.assertRaises(TypeError) as exc:
            pidinst.owners = owners    
        self.assertEqual(str(exc.exception), "owners must be a list of Owner objects")    

    def test_valid_owner_object_append(self):
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        owner = Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type="HostingInstitution")
        owner_identifier = OwnerIdentifier(owner_identifier_value="0000-ABCD-1234-WXYZ", owner_identifier_type='ORCID') 
        owner.owner_identifier = owner_identifier
        pidinst.append_owner(owner)

        self.assertIsInstance(pidinst, PIDInst, 'Something went wrong with class instantation')
        self.assertIsInstance(pidinst.owners[0], Owner, 'Something went wrong with class instantation')

    def test_non_owner_object_append(self):
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        dummy_owner = {'name':'Jane Doe'}
        with self.assertRaises(TypeError) as exc:
            pidinst.append_owner(dummy_owner)
        self.assertEqual(str(exc.exception), "owner must be instance of Owner class")

    # INSTRUMENT MANUFACTURER TESTS
    def test_valid_manufacturer_object_set_on_init(self):
        manufacturers = []
        manufacturer = Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="Organizational")
        manufacturer_identifier = ManufacturerIdentifier(manufacturer_identifier_value="https://www.acme.com", manufacturer_identifier_type='URL') 
        manufacturer.manufacturer_identifier = manufacturer_identifier
        manufacturers.append(manufacturer)

        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst', manufacturers=manufacturers)        

        self.assertIsInstance(pidinst, PIDInst, 'Something went wrong with class instantation')
        self.assertIsInstance(pidinst.manufacturers[0], Manufacturer, 'Something went wrong with class instantation')

    def test_invalid_non_manufacturer_object_set_on_init(self):
        manufacturers = []
        manufacturer = {'manufacturer_identifier_value':"https://www.acme.com", 'manufacturer_identifier_type':'URL'}
        manufacturers.append(manufacturer)

        with self.assertRaises(TypeError) as exc:
            PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst', manufacturers=manufacturers)    
        self.assertEqual(str(exc.exception), "manufacturers must be a list of Manufacturer objects")    

    def test_invalid_non_manufacturer_object_set_post_init(self):
        manufacturers = []
        manufacturer = {'manufacturer_identifier_valu':"https://www.acme.com", 'manufacturer_identifier_type':'URL'}
        manufacturers.append(manufacturer)
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        self.assertIsInstance(pidinst, PIDInst, 'Something went wrong with class instantation')

        with self.assertRaises(TypeError) as exc:
            pidinst.manufacturers = manufacturers    
        self.assertEqual(str(exc.exception), "manufacturers must be a list of Manufacturer objects") 

    def test_valid_manufacturer_object_append(self):
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        manufacturer = Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="Organizational")
        manufacturer_identifier = ManufacturerIdentifier(manufacturer_identifier_value="https://www.acme.com", manufacturer_identifier_type='URL') 
        manufacturer.manufacturer_identifier = manufacturer_identifier
        pidinst.append_manufacturer(manufacturer)

        self.assertIsInstance(pidinst, PIDInst, 'Something went wrong with class instantation')
        self.assertIsInstance(pidinst.manufacturers[0], Manufacturer, 'Something went wrong with class instantation')

    def test_non_manufacturer_object_append(self):
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        dummy_manufacturer = {'name':'Manufacturer X'}
        with self.assertRaises(TypeError) as exc:
            pidinst.append_manufacturer(dummy_manufacturer)
        self.assertEqual(str(exc.exception), "manufacturer must be instance of Manufacturer class")

    # INSTRUMENT RELATED IDENTIFIER TESTS
    def test_valid_related_identifier_object_set_on_init(self):
        related_identifiers = []
        related_identifier = RelatedIdentifier(related_identifier_value="https://www.pathtopaper.edu.au", related_identifier_type="URL", related_identifier_relation_type="IsDescribedBy", related_identifier_name="Documentation Paper")
        related_identifiers.append(related_identifier)
        pidinst = PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst', related_identifiers=related_identifiers)        

        self.assertIsInstance(pidinst, PIDInst, 'Something went wrong with class instantation')
        self.assertIsInstance(pidinst.related_identifiers[0], RelatedIdentifier, 'Something went wrong with class instantation')

    def test_invalid_non_related_identifier_object_set_on_init(self):
        related_identifiers = []
        related = {'related_identifier_value':"https://www.pathtopaper.edu.au", 'related_identifier_type':'URL'}
        related_identifiers.append(related)

        with self.assertRaises(TypeError) as exc:
            PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst', related_identifiers=related_identifiers)    
        self.assertEqual(str(exc.exception), "related_identifiers must be a list of RelatedIdentifier objects")   

    def test_invalid_non_related_identifier_object_set_post_init(self):
        related_identifiers = []
        related = {'related_identifier_value':"https://www.pathtopaper.edu.au", 'related_identifier_type':'URL'}
        related_identifiers.append(related)
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        self.assertIsInstance(pidinst, PIDInst, 'Something went wrong with class instantation')

        with self.assertRaises(TypeError) as exc:
            pidinst.related_identifiers = related_identifiers    
        self.assertEqual(str(exc.exception), "related_identifiers must be a list of RelatedIdentifier objects") 

    def test_valid_related_identifier_object_append(self):
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        related_identifier_1 = RelatedIdentifier(related_identifier_value="https://www.pathtopaper.edu.au", related_identifier_type="URL", related_identifier_relation_type="IsDescribedBy", related_identifier_name="Documentation Paper")
        pidinst.append_related_identifier(related_identifier_1)
        related_identifier_2 = RelatedIdentifier(related_identifier_value="https://www.pathtopaper.edu.au", related_identifier_type="URL", related_identifier_relation_type="IsDescribedBy", related_identifier_name="Documentation Paper")
        pidinst.append_related_identifier(related_identifier_2)

        self.assertIsInstance(pidinst, PIDInst, 'Something went wrong with class instantation')
        self.assertIsInstance(pidinst.related_identifiers[0], RelatedIdentifier, 'Something went wrong with class instantation')
        self.assertIsInstance(pidinst.related_identifiers[1], RelatedIdentifier, 'Something went wrong with class instantation')

    def test_non_related_identifier_object_append(self):
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        dummy_related_identifier = {'name':'Paper X'}
        with self.assertRaises(TypeError) as exc:
            pidinst.append_related_identifier(dummy_related_identifier)
        self.assertEqual(str(exc.exception), "related_identifier must be instance of RelatedIdentifier class")

    # INSTRUMENT MODEL TESTS
    def test_valid_model_object_set(self):
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        model = Model(model_name="Model OPQ")
        model_identifier = ModelIdentifier(model_identifier_value="ABC123", model_identifier_type='URL') 
        model.model_identifier = model_identifier
        pidinst.model = model

        self.assertIsInstance(pidinst, PIDInst, 'Something went wrong with class instantation')
        self.assertIsInstance(pidinst.model, Model, 'Something went wrong with class instantation')

    def test_non_model_object_set(self):
        pidinst =  PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description='A description of this pidinst')        
        dummy_model = {'name':'Manufacturer X'}
        with self.assertRaises(TypeError) as exc:
            pidinst.model = dummy_model
        self.assertEqual(str(exc.exception), "model must be instance of Model class")

    # DESCRIPTION TESTS
    def test_non_string_description_error(self):
        with self.assertRaises(TypeError) as exc:
            PIDInst(landing_page="https://mylandingpage.com", name='Instrument XYZ', description=33)
        self.assertEqual(str(exc.exception), "description must be a string")


class TestIdentifiers(unittest.TestCase):

    def test_valid_identifier_doi(self):
        identifier = Identifier(identifier_value="10.1000/ABC123", identifier_type="DOI")
        self.assertIsInstance(identifier, Identifier, 'Something went wrong with Identifier class instantation')

    def test_valid_identifier_handle(self):
        identifier = Identifier(identifier_value="2381/12345", identifier_type="Handle")
        self.assertIsInstance(identifier, Identifier, 'Something went wrong with Identifier class instantation')

    def test_empty_identifier_type(self):
        with self.assertRaises(ValueError) as exc:
            Identifier(identifier_value="2381/12345")
        self.assertEqual(str(exc.exception), "Identifier Type cannot be None")

    def test_invalid_identifier_type_type(self):
        with self.assertRaises(TypeError) as exc:
            Identifier(identifier_value="2381/12345", identifier_type=321)
        self.assertEqual(str(exc.exception), "Identifier Type must be a string")

    def test_invalid_identifier_type(self):
        with self.assertRaises(ValueError) as exc:
            Identifier(identifier_value="2381/12345", identifier_type="DUMMY")
        self.assertEqual(str(exc.exception), "Identifier Type not recognised")

    def test_empty_identifier_value(self):
        with self.assertRaises(ValueError) as exc:
            Identifier(identifier_type="DOI")
        self.assertEqual(str(exc.exception), "Identifier Value cannot be None")

    def test_invalid_identifier_value_type(self):
        with self.assertRaises(TypeError) as exc:
            Identifier(identifier_value=123, identifier_type="DOI")
        self.assertEqual(str(exc.exception), "Identifier Value must be a string")

    def test_invalid_identifier_value_empty(self):
        with self.assertRaises(ValueError) as exc:
            Identifier(identifier_value='', identifier_type="DOI")
        self.assertEqual(str(exc.exception), "Identifier Value cannot be an empty string")

    def test_identifier_value_too_long_error(self):
        with self.assertRaises(ValueError) as exc:
            Identifier(identifier_value="A"*200, identifier_type='DOI')
        self.assertEqual(str(exc.exception), "Identifier Value must be less than 200 chars")


class TestOwners(unittest.TestCase):

    def test_valid_owner(self):
        owner = Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type="HostingInstitution")
        owner_identifier = OwnerIdentifier(owner_identifier_value="0000-ABCD-1234-WXYZ", owner_identifier_type='ORCID') 
        owner.owner_identifier = owner_identifier
        self.assertIsInstance(owner, Owner, 'Something went wrong with owner class instantation')

    def test_valid_owner_no_identifier(self):
        owner = Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type="HostingInstitution")
        self.assertIsInstance(owner, Owner, 'Something went wrong with owner class instantation')

    def test_invalid_no_owner_name(self):
        with self.assertRaises(ValueError) as exc:
            Owner(owner_contact="jane.doe@email.com", owner_type="HostingInstitution")
        self.assertEqual(str(exc.exception), "owner_name cannot be None")

    def test_invalid_empty_owner_name(self):
        with self.assertRaises(ValueError) as exc:
            Owner(owner_name="", owner_contact="jane.doe@email.com", owner_type="HostingInstitution")
        self.assertEqual(str(exc.exception), "Owner name cannot be an empty string")

    def test_invalid_no_owner_type(self):
        with self.assertRaises(ValueError) as exc:
            Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com")
        self.assertEqual(str(exc.exception), "owner_type cannot be None")

    def test_invalid_empty_owner_type(self):
        with self.assertRaises(ValueError) as exc:
            Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type="")
        self.assertEqual(str(exc.exception), "Owner type cannot be an empty string")

    def test_invalid_owner_type_invalid(self):
        with self.assertRaises(ValueError) as exc:
            Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type="Experimenter")
        self.assertEqual(str(exc.exception), "owner_type is not valid")

    def test_invalid_set_owner_identifier(self):
        owner = Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type="HostingInstitution")
        owner_identifier = {'name':'DUMMY'}
        with self.assertRaises(TypeError) as exc:
            owner.owner_identifier = owner_identifier
        self.assertEqual(str(exc.exception), "owner_identifier must be instance of OwnerIdentifier class")


class TestOwnerIdentifiers(unittest.TestCase):

    def test_invalid_empty_owner_identifier_value(self):
        with self.assertRaises(ValueError) as exc:
            OwnerIdentifier(owner_identifier_value=None, owner_identifier_type=None) 
        self.assertEqual(str(exc.exception), "Owner Identifier Value cannot be None")

    def test_invalid_no_owner_identifier_type(self):
        with self.assertRaises(ValueError) as exc:
            OwnerIdentifier(owner_identifier_value='0000-1111-2222-3333', owner_identifier_type=None) 
        self.assertEqual(str(exc.exception), "Owner Identifier Type cannot be None")

    def test_invalid_owner_identifier_type(self):
        with self.assertRaises(ValueError) as exc:
            OwnerIdentifier(owner_identifier_value="0000-ABCD-1234-WXYZ", owner_identifier_type='DUMMY') 
        self.assertEqual(str(exc.exception), "Owner Identifier Type not recognised")


class TestManufacturers(unittest.TestCase):

    def test_valid_manufacturer(self):
        manufacturer = Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="Organizational")
        manufacturer_identifier = ManufacturerIdentifier(manufacturer_identifier_value="https://www.acme.com", manufacturer_identifier_type='URL') 
        manufacturer.manufacturer_identifier = manufacturer_identifier
        self.assertIsInstance(manufacturer, Manufacturer, 'Something went wrong with manufacturer class instantation')

    def test_valid_manufacturer_no_identifier(self):
        manufacturer = Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="Organizational")
        self.assertIsInstance(manufacturer, Manufacturer, 'Something went wrong with manufacturer class instantation')

    def test_invalid_manufacturer_empty_name(self):
        with self.assertRaises(ValueError) as exc:
            Manufacturer(manufacturer_name="", manufacturer_name_type="Organizational")
        self.assertEqual(str(exc.exception), "manufacturer_name cannot be an empty string")

    def test_invalid_set_manufacturer_identifier(self):
        manufacturer = Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="Organizational")
        manufacturer_identifier = {'value':'DUMMY'}
        with self.assertRaises(TypeError) as exc:
            manufacturer.manufacturer_identifier = manufacturer_identifier
        self.assertEqual(str(exc.exception), "manufacturer_identifier must be instance of ManufacturerIdentifier class")

    def test_invalid_no_manufacturer_name_type(self):
        with self.assertRaises(ValueError) as exc:
            Manufacturer(manufacturer_name="Acme Inc")
        self.assertEqual(str(exc.exception), "manufacturer_name_type cannot be None")

    def test_invalid_empty_manufacturer_name_type(self):
        with self.assertRaises(ValueError) as exc:
            Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="")
        self.assertEqual(str(exc.exception), "manufacturer_name_type not recognised")

    def test_invalid_manufacturer_name_type_invalid(self):
        with self.assertRaises(ValueError) as exc:
            Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="INVALID TYPE")
        self.assertEqual(str(exc.exception), "manufacturer_name_type not recognised")


class TestManufacturerIdentifiers(unittest.TestCase):
    
    def test_invalid_empty_manufacturer_identifier_value(self):
        with self.assertRaises(ValueError) as exc:
            ManufacturerIdentifier(manufacturer_identifier_value=None, manufacturer_identifier_type=None) 
        self.assertEqual(str(exc.exception), "Manufacturer Identifier Value cannot be None")

    def test_invalid_empty_manufacturer_identifier_type(self):
        with self.assertRaises(ValueError) as exc:
            ManufacturerIdentifier(manufacturer_identifier_value='0000-1111-2222-3333', manufacturer_identifier_type=None) 
        self.assertEqual(str(exc.exception), "Manufacturer Identifier Type cannot be None")

    def test_invalid_manufacturer_identifier_type(self):
        with self.assertRaises(ValueError) as exc:
            ManufacturerIdentifier(manufacturer_identifier_value="0000-ABCD-1234-WXYZ", manufacturer_identifier_type='DUMMY') 
        self.assertEqual(str(exc.exception), "Manufacturer Identifier Type not recognised")


class TestModels(unittest.TestCase):

    def test_valid_model_with_identifier(self):
        model = Model(model_name="Acme Inc")
        model_identifier = ModelIdentifier(model_identifier_value="ABC123", model_identifier_type='URL') 
        model.model_identifier = model_identifier
        self.assertIsInstance(model, Model, 'Something went wrong with model class instantation')

    def test_valid_model_without_identifier(self):
        model = Model(model_name="Acme Inc")
        self.assertIsInstance(model, Model, 'Something went wrong with model class instantation')

    def test_invalid_model_empty_name(self):
        with self.assertRaises(ValueError) as exc:
            Model(model_name="")
        self.assertEqual(str(exc.exception), "model_name cannot be an empty string")

    def test_model_identifier_replace(self):
        model = Model(model_name="Acme Inc")
        model_identifier_1 = ModelIdentifier(model_identifier_value="ABC123", model_identifier_type='URL') 
        model.model_identifier = model_identifier_1
        
        model_identifier_2 = ModelIdentifier(model_identifier_value="DEF456", model_identifier_type='URL') 
        model.model_identifier = model_identifier_2
        
        self.assertEqual(model.model_identifier.model_identifier_value, "DEF456")


class TestModelIdentifiers(unittest.TestCase):
    
    def test_invalid_empty_model_identifier_value(self):
        with self.assertRaises(ValueError) as exc:
            ModelIdentifier(model_identifier_value=None, model_identifier_type=None) 
        self.assertEqual(str(exc.exception), "Model Identifier Value cannot be None")

    def test_invalid_empty_model_identifier_type(self):
        with self.assertRaises(ValueError) as exc:
            ModelIdentifier(model_identifier_value='XYZ123', model_identifier_type=None) 
        self.assertEqual(str(exc.exception), "Model Identifier Type cannot be None")

    def test_invalid_model_identifier_value(self):
        with self.assertRaises(TypeError) as exc:
            ModelIdentifier(model_identifier_value=123, model_identifier_type='a model identfier type') 
        self.assertEqual(str(exc.exception), "Model Identifier Value must be a string")

    def test_invalid_model_identifier_type(self):
        with self.assertRaises(TypeError) as exc:
            ModelIdentifier(model_identifier_value='XYZ123', model_identifier_type=123) 
        self.assertEqual(str(exc.exception), "Model Identifier Type must be a string")


class TestRelatedIdentifiers(unittest.TestCase):

    def test_valid_related_identifier(self):
        related_identifier = RelatedIdentifier(related_identifier_value="https://www.pathtopaper.edu.au", related_identifier_type="URL", related_identifier_relation_type="IsDescribedBy", related_identifier_name="Documentation Paper")
        self.assertIsInstance(related_identifier, RelatedIdentifier, 'Something went wrong with related identifier class instantation')

    def test_valid_related_identifier_no_name(self):
        related_identifier = RelatedIdentifier(related_identifier_value="https://www.pathtopaper.edu.au", related_identifier_type="URL", related_identifier_relation_type="IsDescribedBy")
        self.assertIsInstance(related_identifier, RelatedIdentifier, 'Something went wrong with related identifier class instantation')

    def test_invalid_no_value(self):
        with self.assertRaises(ValueError) as exc:
            RelatedIdentifier(related_identifier_type="URL", related_identifier_relation_type="IsDescribedBy")
        self.assertEqual(str(exc.exception), "related_identifier_value cannot be None")

    def test_invalid_empty_value(self):
        with self.assertRaises(ValueError) as exc:
            RelatedIdentifier(related_identifier_value="", related_identifier_type="URL", related_identifier_relation_type="IsDescribedBy", related_identifier_name="Documentation Paper")
        self.assertEqual(str(exc.exception), "related_identifier_value cannot be an empty string")

    def test_invalid_no_identifier_type(self):
        with self.assertRaises(ValueError) as exc:
            RelatedIdentifier(related_identifier_value="https://www.pathtopaper.edu.au", related_identifier_relation_type="IsDescribedBy")
        self.assertEqual(str(exc.exception), "related_identifier_type cannot be None")

    def test_invalid_identifier_type(self):
        with self.assertRaises(ValueError) as exc:
            RelatedIdentifier(related_identifier_value="https://www.pathtopaper.edu.au", related_identifier_type="ABC", related_identifier_relation_type="IsDescribedBy")
        self.assertEqual(str(exc.exception), "Related Identifier Type not recognised")

    def test_invalid_no_relation_type(self):
        with self.assertRaises(ValueError) as exc:
            RelatedIdentifier(related_identifier_value="https://www.pathtopaper.edu.au", related_identifier_type="URL")
        self.assertEqual(str(exc.exception), "related_identifier_relation_type cannot be None")

    def test_invalid_relation_type(self):
        with self.assertRaises(ValueError) as exc:
            RelatedIdentifier(related_identifier_value="https://www.pathtopaper.edu.au", related_identifier_type="URL", related_identifier_relation_type="ABCDEF")
        self.assertEqual(str(exc.exception), "Related Identifier Relation Type not recognised")


class TestValidations(unittest.TestCase):

    def test_valid_pidinst(self):
        # Initialise Instrument
        pidinst = PIDInst(
            landing_page='https://www.landingpage.com', 
            name="Instrument XYZ", 
        )
        # Identifier
        identifier = Identifier(identifier_value="10.1000/retwebwb", identifier_type="DOI")
        pidinst.identifier = identifier
        # Manufacturer
        manufacturer = Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="Organizational")
        manufacturer_identifier = ManufacturerIdentifier(manufacturer_identifier_value="https://www.acme.com", manufacturer_identifier_type='URL') 
        manufacturer.manufacturer_identifier = manufacturer_identifier
        pidinst.append_manufacturer(manufacturer)
        # Owner
        owner = Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type="HostingInstitution")
        owner_identifier = OwnerIdentifier(owner_identifier_value="0000-ABCD-1234-WXYZ", owner_identifier_type='ORCID') 
        owner.owner_identifier = owner_identifier
        pidinst.append_owner(owner)

        self.assertTrue(pidinst.is_valid_pidinst, 'Something went wrong with PIDInst validation')

    def test_invalid_pidinst_1(self):
        # Initialise Instrument
        pidinst = PIDInst(
            landing_page='https://www.landingpage.com', 
            name="Instrument XYZ", 
        )
        # Manufacturer
        manufacturer = Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="Organizational")
        manufacturer_identifier = ManufacturerIdentifier(manufacturer_identifier_value="https://www.acme.com", manufacturer_identifier_type='URL') 
        manufacturer.manufacturer_identifier = manufacturer_identifier
        pidinst.append_manufacturer(manufacturer)
        # Owner
        owner = Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type="HostingInstitution")
        owner_identifier = OwnerIdentifier(owner_identifier_value="0000-ABCD-1234-WXYZ", owner_identifier_type='ORCID') 
        owner.owner_identifier = owner_identifier
        pidinst.append_owner(owner)

        self.assertFalse(pidinst.is_valid_pidinst(), 'Something went wrong with PIDInst validation')

    def test_invalid_pidinst_2(self):
        # Initialise Instrument
        pidinst = PIDInst(
            landing_page='https://www.landingpage.com', 
            name="Instrument XYZ", 
        )
        # Identifier
        identifier = Identifier(identifier_value="10.1000/retwebwb", identifier_type="DOI")
        pidinst.identifier = identifier
        # Manufacturer
        manufacturer = Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="Organizational")
        manufacturer_identifier = ManufacturerIdentifier(manufacturer_identifier_value="https://www.acme.com", manufacturer_identifier_type='URL') 
        manufacturer.manufacturer_identifier = manufacturer_identifier
        pidinst.append_manufacturer(manufacturer)

        self.assertFalse(pidinst.is_valid_pidinst(), 'Something went wrong with PIDInst validation')

    def test_invalid_pidinst_no_owner_type(self):
        # Initialise Instrument
        pidinst = PIDInst(
            landing_page='https://www.landingpage.com', 
            name="Instrument XYZ", 
        )
        # Identifier
        identifier = Identifier(identifier_value="10.1000/retwebwb", identifier_type="DOI")
        pidinst.identifier = identifier
        # Manufacturer
        manufacturer = Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="Organizational")
        manufacturer_identifier = ManufacturerIdentifier(manufacturer_identifier_value="https://www.acme.com", manufacturer_identifier_type='URL') 
        manufacturer.manufacturer_identifier = manufacturer_identifier
        pidinst.append_manufacturer(manufacturer)
        # Owner
        owner = Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type="ContactPerson")
        owner_identifier = OwnerIdentifier(owner_identifier_value="0000-ABCD-1234-WXYZ", owner_identifier_type='ORCID') 
        owner.owner_identifier = owner_identifier
        pidinst.append_owner(owner)

        self.assertFalse(pidinst.is_valid_pidinst(), 'Something went wrong with PIDInst validation')


class TestInstruments(unittest.TestCase):
    
    def test_valid_instrument(self):
        # Initialise Instrument
        instrument = Instrument(
            landing_page='https://www.landingpage.com', 
            name="Instrument XYZ", 
        )
        # Identifier
        identifier = Identifier(identifier_value="10.1000/retwebwb", identifier_type="DOI")
        instrument.identifier = identifier
        # Manufacturer
        manufacturer = Manufacturer(manufacturer_name="Acme Inc", manufacturer_name_type="Organizational")
        manufacturer_identifier = ManufacturerIdentifier(manufacturer_identifier_value="https://www.acme.com", manufacturer_identifier_type='URL') 
        manufacturer.manufacturer_identifier = manufacturer_identifier
        instrument.append_manufacturer(manufacturer)
        # Owner
        owner = Owner(owner_name="Jane Doe", owner_contact="jane.doe@email.com", owner_type ="HostingInstitution")
        owner_identifier = OwnerIdentifier(owner_identifier_value="0000-ABCD-1234-WXYZ", owner_identifier_type='ORCID') 
        owner.owner_identifier = owner_identifier
        instrument.append_owner(owner)

        self.assertTrue(instrument.is_valid_pidinst, 'Something went wrong with Instrument validation')

    # TEST DOI ALLOCATION
    def test_allocate_doi_identifier_exists(self):
        identifier = Identifier(identifier_value="10.1000/retwebwb", identifier_type="DOI")
        instrument = Instrument(
            landing_page='https://www.landingpage.com', 
            name="Instrument XYZ" 
        )
        instrument.identifier = identifier
        with self.assertRaises(ValueError) as exc:
            instrument.allocate_doi()
        self.assertEqual(str(exc.exception), "This Instrument record already has an identifier allocated")
   
    def test_allocate_doi_non_complete_info(self):
        instrument = Instrument(
            landing_page='https://www.landingpage.com', 
            name="Instrument XYZ"
        )
        with self.assertRaises(ValueError) as exc:
            instrument.allocate_doi()
        self.assertEqual(str(exc.exception), "This record does not yet have sufficient content to allocate a DOI")
   
    def test_allocate_doi_complete_info(self):
        pass


if __name__ == '__main__':
    unittest.main()
