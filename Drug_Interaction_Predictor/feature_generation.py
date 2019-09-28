import rdkit as rd
from rdkit import Chem
from rdkit.Chem import AllChem
import numpy as np


# 
#
#


def smiles_to_ECFP(smiles, fp_radius = 2):
    '''Convert a SMILES representation to ECFP representation

    
    '''
    
    if smiles is not None:
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, fp_radius)
        else:
            return None
        fparr = np.zeros((1,))
        rd.DataStructs.ConvertToNumpyArray(fp, fparr)
    else:
        return None

    fparr = np.reshape(fparr, (-1, 1))
    
    return fparr

# TODO : Optional arguments for smiles_feature_generator?

def featurize_smiles_and_interactions(relation_list, smiles_feature_generator, smiles_dict, label_map):
    '''Generate numerical features from smiles data and label interactions


    '''

    feature_dict = {}
    smiles_feature_list = []
    interaction_label_list = []
    drug_pair_list = []

    for relation in relation_list:
        sub, obj, interaction = relation.subject, relation.object, relation.normalized_relation

        sub_smiles, obj_smiles = smiles_dict[sub], smiles_dict[obj]

        if sub_smiles not in feature_dict:
            feature_dict[sub_smiles] = smiles_feature_generator(sub_smiles)
        sub_feature = feature_dict[sub_smiles]

        if obj_smiles not in feature_dict:
            feature_dict[obj_smiles] = smiles_feature_generator(obj_smiles)
        obj_feature = feature_dict[obj_smiles]

        interaction_label = label_map[interaction]

        if sub_feature is not None and obj_feature is not None:
            smiles_feature_list.append(np.concatenate((sub_feature, obj_feature)))
            interaction_label_list.append(interaction_label)
            drug_pair_list.append((sub, obj))
        

    return smiles_feature_list, interaction_label_list, drug_pair_list


