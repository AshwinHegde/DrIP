import xml.etree.ElementTree as ET
import pandas as pd
from collections import defaultdict
import csv

def dict_to_tuple_list(d):
    '''
    Convert a list of tuples to a dictionary
    '''
    return [(k, *t) for k, v in d.items() for t in v]



def drug_reader(xml_file, number_of_drugs = 10):
    '''
    Parses an XML file iteratively and returns a tuple list of interacting drugs with their descriptions and a dictionary of drugs with their SMILES representations.
    Input :
        xml_file -- Address of XML file to be parsed
        number_of_drugs -- Number of drugs to be read

    Output :
        interaction_list -- A list of tuples with each tuple containing two drugs and a description of the interaction between them
        smiles_dict -- A dictionary of drugs and the corresponding SMILES string
        drug_count -- Total number of drugs read
        interaction_count -- Total number of interaction pairs generated
    '''
    parser = ET.iterparse(xml_file, events = ('start', 'end'))
    add = '{http://www.drugbank.ca}'
    path = []
    interaction_dict = defaultdict(list)
    smiles_dict = {}
    interaction_count = 0
    drug_count = 0
    skip_drug = False
    for event, elem in parser:

        #Detect start of a tag
        if event == 'start':
            # Find each drug and record the name of the main drug
            if elem.tag == add+'drug' and len(path) == 1:
                if elem.find(add+'name') is not None:
                    drug_a = elem.find(add+'name').text
                    #print('Main drug : ', drug_a)
                    smiles = ''
                else:
                    skip_drug = True

            # Keep track of node hierarchy. Path will look like [parent child grandchild ...]
            path.append(elem.tag)

            # Find the SMILES representation of the drug
            if add+'calculated-properties' in path:
                if elem.tag == add+'property':
                    if elem.find(add+'kind') is not None:
                        if elem.find(add+'kind').text == 'SMILES':
                            if elem.find(add+'value') is not None:
                                smiles = elem.find(add+'value').text
                                smiles_dict[drug_a] = smiles
                                #print('SMILES Representation : ', elem.find(add+'value').text)


            # Find all the drugs that interact with the main drug and the descriptionof the interaction
            if path[-1] == add+'drug-interaction' and not skip_drug:
                if elem.find(add+'name') is None:
                    pass
                elif elem.find(add+'description') is None:
                    pass
                else:
                    drug_b = elem.find(add+'name').text
                    interaction_desc = elem.find(add+'description').text
                    # Skip duplicate pairings. For example if drug A interacts with drug B, avoid drug B interacts with drug A
                    if drug_b not in interaction_dict:
                        interaction_dict[drug_a].append([drug_b, interaction_desc])
                        interaction_count += 1

        # Detect end tag
        elif event == 'end':

            path.pop()

            if len(path) == 1:
                drug_count += 1
                skip_drug = False
                #print('Drug count : ', drug_count)
                #print('Drug interactions so far : ', interaction_count)
                if drug_count >= number_of_drugs:
                    break

    interaction_list = dict_to_tuple_list(interaction_dict)

    interaction_df = pd.DataFrame(interaction_list, columns = ['Drug A', 'Drug B', 'Interaction Description'])

    return interaction_df, smiles_dict, drug_count, interaction_count

def remove_non_smiles(interaction_df, smiles_dict):
    '''
    Add a column to input dataframe with the corresponding SMILES representations obtained from the input dictionary.
    Input :
        interaction_df -- Dataframe with two drugs and a description of their interaction
        smiles_dict -- Dictionary mapping names of drugs to their SMILES representations

    Output :
        Dataframe with columns added for SMILES representation of each drug. None if no representation found.
    '''
    interaction_df['SMILES A'] = interaction_df.apply(lambda row: smiles_dict.get(row.loc['Drug A']), axis = 1)
    interaction_df['SMILES B'] = interaction_df.apply(lambda row: smiles_dict.get(row.loc['Drug B']), axis = 1)
    return interaction_df.dropna(axis = 0)

def write_dict_to_csv_file(csv_file, d):
    try:
        with open(csv_file, 'w') as file:
            w = csv.writer(file)
            w.writerows(d.items())
    except IOError:
        print('I/O Error')

def main():
    '''
    Read drugs, interaction pairs and SMILES representations. Then remove drugs with missing SMILES data. Lastly write the data into a csv file.
    '''

    xml_file = '/home/ashwin/datasets/drugbank_data/drugbank_data.xml'

    print('Reading drugs from DrugBank data ...')
    interaction_df, smiles_dict, drug_count, interaction_count = drug_reader(xml_file, 500)
    print('Drugs read : ', drug_count)
    print('Interaction pairs : ', interaction_count)

    print('Removing drugs without structural data ... ')
    interaction_smiles_df = remove_non_smiles(interaction_df, smiles_dict)
    print('Interaction pairs retained : ', len(interaction_smiles_df))

    write_dict_to_csv_file('/home/ashwin/repos/Insight_Project_Framework/data/preprocessed/interaction_smiles.csv', interaction_smiles_df)

if __name__ == '__main__':
    main()
