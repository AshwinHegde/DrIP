# Drug Interaction Predictor (DrIP)
### What is it about?
This project tries to predict the kind of effect that occurs when two drugs are taken in conjunction, purely from their molecular structure. 

## Usage
DrIP can be used in multiple ways. Please use as suited to your needs.
### Web Application
The web application can be accessed at [DrIP](http://mlsolver.xyz/DrIP). This is good for one-off predictions and using a graphical interface.
Upload image

Use the molecular editor on the left to draw the candidate drug molecule. Use the dropdown list on the right to choose an existing drug from the DrugBank database. Clicking on the predict button then gives the top five predicted interactions and the probabilities predicted by the model.
### Local
To run bulk predictions, DrIP can be used locally. 
#### Creating a Conda environment
To setup a conda environment and run predictions follow the instructions below.
Clone the repository

	git clone https://github.com/AshwinHegde/DrIP

Create a conda environment from the environment.yml file and activate the environment

	cd DrIP
	conda env create -n DrIP -f environment.yml
	source activate DrIP

Next download the pre-trained model

	bash download_model.sh

Now you are good to go.

### Inference
Predictions from the command line are made using the `predict_cli.py` file.

	python Drug-Interaction-Predictor/predict_cli.py --candidates_file [candidates.txt] --drugs_file [drugs.txt] --target_file [output.csv] --model [model_file]

* `candidates_file` - path to the file of candidate drug SMILES strings. This file should be a `.txt` file. It must contain one SMILES string per line.
* `drugs_file` - path to the file of existing drug SMILES strings. This file should also be a `.txt` file and contain one SMILES string per line.
* `target_file` - path to the output file which will contain interactions for each pair of drugs from `candidates_file` and `drugs_file`. This file should be a `.csv` file.
* `model` (optional) - path to the model file used for predictions. By default uses the model downloaded. Change this if you want to use your own model.

To test the CLI, you can use the sample data provided. Simply run 

	python Drug-Interaction-Predictor/predict_cli.py -c data/sample/candidates.txt -d data/sample/drugs.txt -t interactions.csv


## Getting data
Data is obtained from [DrugBank](https://www.drugbank.ca/), a comprehensive drug database. The data is available for free for academic and non-commercial purposes. If you are interested, data can be requested from DrugBank on their website. The data obtained is in XML format.

[Wishart DS et al. : DrugBank 5.0: a major update to the DrugBank database for 2018. Nucleic Acids Res. 2018 Jan 4;46(D1):D1074-D1082.](https://www.ncbi.nlm.nih.gov/pubmed/29126136)

## Attribution
Special thanks to Shristi Pandey whose project [Diction](https://github.com/ShristiP/diction) got me interested originally in this subject. I have built on her codebase.
