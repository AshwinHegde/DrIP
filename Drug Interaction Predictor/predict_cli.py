import argparse
import sys
from inference import *
import tensorflow as tf

parser = argparse.ArgumentParser()
parser.add_argument("--candidates_file", help="Path to file with candidate SMILES strings\
     (txt file)")
parser.add_argument("--drugs_file", help="Path to file with drug SMILES strings \
    (txt file)")
parser.add_argument("--target_file", help="Path to target file to save interactions \
    (csv file)")
parser.add_argument("--model", help="Path to model to use for predictions \
    (csv file)", default='mlp_ECFP.h5')
args = parser.parse_args()

candidates_file = args.candidates_file
drugs_file = args.drugs_file
target_file = args.target_file

if candidates_file[-4:] != '.txt':
    raise ValueError('Candidates file must be a txt file')

if drugs_file[-4:] != '.txt':
    raise ValueError('Drugs file must be a txt file')

if target_file[-4:] != '.csv':
    raise ValueError('Target file must be a csv file')

model = tf.keras.models.load_model(args.model)

predict_from_files(candidates_file, drugs_file, target_file, model)