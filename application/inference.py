import tensorflow as tf
from feature_generation import smiles_to_ECFP
import numpy as np
import pandas as pd

# File that contains inference functions
#


def predict_interaction(smiles, smiles_b, model = 'mlp', feature = 'ECFP', directory = ''):
    '''Use model to predict interaction

    Args :

    Returns :
    '''

# TODO : os.path
    print('Loading model ...')
    model_path = directory + '/' + model + '_' + feature + '.h5'
    model = tf.keras.models.load_model(model_path)
    print('Model loaded.')

    vec_a = smiles_to_ECFP(smiles)
    vec_b = smiles_to_ECFP(smiles_b)
    test = np.concatenate((vec_a, vec_b)).reshape((1, -1))
    prediction = model.predict(test)

    return prediction


def get_top_n(arr, n):
    '''Return the top n elements and indices of a numpy array

    Args :

    Returns :
    '''

    assert(type(n) == int and n > 0)
    arr_df = pd.DataFrame(data = arr[0], columns = ['Probabilities'])
    arr_df.sort_values('Probabilities', ascending = False, inplace = True)
    top_labels = list(arr_df[:n].index)
    top_probs = list(arr_df[:5]['Probabilities'])
    return top_labels, top_probs


if __name__ == '__main__':
    smiles = 'CC2COc1ccccc1N2C(=O)C(Cl)Cl'#input()
    smiles_b = 'N#CC(=O)CC(=O)CC(=O)O'#input()
    prediction = predict_interaction(smiles, smiles_b)
    label = np.argmax(prediction)
    print(prediction.shape)
    print('Classification label : {} , probablilty : {}'.format(label, prediction[0, label]))
    print(prediction)
    labels, probs = get_top_n(prediction, 5)
    print(*zip(labels, probs))