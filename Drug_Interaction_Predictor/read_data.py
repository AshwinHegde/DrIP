import boto3
import botocore
import lxml.etree as et
import xml.etree.ElementTree as ET


# TODO : Paths are included as arguments to read functions.
# Maybe include this in an external file that user can modify
# TODO : Improve documentation.


# Contains functions to read data from XML file obtained from DrugBank.
# Separate functions to read locally and to read from S3 storage.
#
# Defines a Drug class that for my purposes has name, structure
# and interactions as attributes. The XML file from DrugBank has
# much more information than read here and if necessary these can
# be added to the class definition. Note that then, extra commands
# must be written into read_data to read these attributes.
# 
# Read functions return a list of Drug objects and a dictionary
# of drug names with corresponding SMILES representations.

# Also defines an Interaction class that contains the names of
# two drugs, their SMILES representation and a textual description
# of their interaction.

# A function (get_interaction) returns a list of all interactions
# (Interaction objects) present in a list of drugs (Drug objects).
# Drugs without structural information are filtered out.



class Drug:
    '''
    Contains relevant features of each drug : Name, SMILES representations and all the drugs it interacts with
    '''
    def __init__(self):
        self.name = None
        self.structure = None
        self.interactions = None

    def __repr__(self):
        return 'Name : {}\nStructure : {}'.format(self.name, self.structure)
    
    # Method to check if drug has structural data
    def has_structure(self):
        if self.structure is not None:
            return True
        else:
            return False


class Interaction:
    '''
    Contains names and SMILES representations of a pair of drugs along with a textual description of the kind of interaction.
    '''
    def __init__(self, druga = None, smilesa = None, drugb = None, smilesb = None, description = None):
        self.druga = druga
        self.smilesa = smilesa
        self.drugb = drugb
        self.smilesb = smilesb
        self.description = description
    
    def __repr__(self):
        return 'Drug A : {}\nSMILES : {}\nDrug B : {}\nSMILES : {}\nInteraction description : {}'.format(self.druga, self.smilesa, self.drugb, self.smilesb, self.description)
    
    def assign(self, druga, smilesa, drugb, smilesb, description):
        self.druga = druga
        self.drugb = drugb
        self.smilesa = smilesa
        self.smilesb = smilesb
        self.description = description


def read_from_bucket(bucket = 'insight-ashwin-s3-bucket', key = 'drugbank_data/drugbank_data.xml', number_of_drugs = 50000):
    '''
    Function to read an XML file from S3 and return a list of Drug objects. It takes as input number of drugs to read, the name of the bucket on S3 and location(key) of the file in the bucket. Invokes read_data function.
    '''
    s3 = boto3.resource('s3', use_ssl = False, verify = False)
    obj = s3.Object(bucket, key)
    file = obj.get()['Body'].read()
    tree = et.ElementTree(et.fromstring(file))
    return read_data(tree, number_of_drugs)


def read_from_file(xml_file, number_of_drugs = 50000):
    '''
    Function to read an XML file locally and return a list of Drug objects. It takes as input the XML file location and number of drugs to be read. Invokes read_data function.
    '''
    tree = ET.parse(xml_file)
    return read_data(tree, number_of_drugs)


def read_data(tree, number_of_drugs = 50000, addon = '{http://www.drugbank.ca}'):
    '''
    Function that takes an ElementTree object as input and parses it to extract relevant features of a drug. Can enter number of drugs to be read and a string(addon) to be added on to all tags depending on XML file. The default addon corresponds to that of DrugBank data. Returns a list of Drug objects.
    '''
    root = tree.getroot()
    drug_count = 0
    drug_list = []
    smiles_dict = {}
    for elem in root:
        drug = Drug()
        # go through the drug descriptions and extract relevant features of each drug : 
        for i in range(len(elem)):
            if elem[i].tag == addon+'name':
                drug.name = (elem[i].text).lower()
                
            if elem[i].tag == addon+'calculated-properties':
                calculated_properties = elem[i]
                for calc_property in calculated_properties:
                    if calc_property[0].text == 'SMILES':
                        drug.structure = calc_property[1].text
                        
            if elem[i].tag ==  addon+'drug-interactions':
                interactions = elem[i]
                drug.interactions = {inter[1].text.lower():inter[2].text for inter in interactions}

        if drug.has_structure():
            drug_list.append(drug)
            smiles_dict[drug.name] = drug.structure
            drug_count += 1
            if drug_count >= number_of_drugs:
                break
    
    return drug_list, smiles_dict


def generate_interactions(drug_list, smiles_dict):
    '''
    Function that takes a list of Drug objects and returns interaction pairs (in terms of Interaction objects) along with their SMILES representation and a textual description of the interaction. A drug name to SMILES dictionary is passed using which drugs without SMILES data are filtered out. Returns a list of Interaction objects.
    '''
    interaction_list = []
    interaction_count = 0
    for drug in drug_list:
        for drugb, description in drug.interactions.items():
            # Only keep drugs that have structural data
            if drugb in smiles_dict:
                interaction = Interaction(drug.name, drug.structure, drugb, smiles_dict[drugb], description)
                interaction_list.append(interaction)
                interaction_count += 1

    return interaction_list