import boto3
import botocore
import lxml.etree as et
import xml.etree.ElementTree as ET

# TODO : Paths are somewhat coded in. Maybe include this in an external file that user can modify

class Drug:
    '''
    Contains relevant features of each drug : Name, SMILES representations and all the drugs it interacts with
    '''
    def __init__(self):
        self.name = None
        self.structure = None
        self.interactions = None

    def __repr__(self):
        return "Name : {}\nStructure : {}".format(self.name, self.structure)
    
    def has_structure(self):
        if self.structure is not None:
            return True
        else:
            return False


def read_from_bucket(number_of_drugs = 50000, bucket = 'insight-ashwin-s3-bucket', key = 'drugbank_data/drugbank_data.xml'):
    '''
    Function to read an XML file from S3 and return a list of Drug objects. It takes as input number of drugs to read, the name of the bucket on S3 and location(key) of the file in the bucket. Invokes read_data function.
    '''
    s3 = boto3.resource('s3', use_ssl = False, verify = False)
    obj = s3.Object(bucket, key)
    file = obj.get()['Body'].read()
    tree = et.ElementTree(et.fromstring(file))
    return read_data(tree)


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
    for elem in root:
        drug = Drug()
        # go through the drug descriptions and extract relevant features of each drug : 
        for i in range(len(elem)):
            if (elem[i].tag == addon+'name'):
                drug.name = (elem[i].text).lower()
                
            if (elem[i].tag == addon+'calculated-properties'):
                calculated_properties = elem[i]
                for calc_property in calculated_properties:
                    if calc_property[0].text == 'SMILES':
                        drug.structure = calc_property[1].text
                        
            if (elem[i].tag ==  addon+'drug-interactions'):
                all_drug_interactions = {}
                drug_interactions = elem[i]
                for drug_interaction in drug_interactions:
                    interacting_drug = (drug_interaction[1].text).lower()
                    description = drug_interaction[2].text
                    all_drug_interactions[interacting_drug] = description
                drug.interactions = all_drug_interactions

        if drug.has_structure():
            drug_list.append(drug)
            drug_count += 1
            if drug_count >= number_of_drugs:
                break
    
    print('Drugs read : ', drug_count)
    return drug_list

def main():
    drug_list = read_from_bucket(number_of_drugs = 10)
    print(drug_list[0][0])

if __name__ == '__main__':
    main()