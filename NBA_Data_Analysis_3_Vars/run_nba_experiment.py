from create_source_target_data import create_all_data
from pre_analyse_NBA import calculate_feature_importance
import papermill as pm
import os
from analyse_NBA_results import create_summary



# Create source and target data
create_all_data()
notebook_folder_path = open('NBA_Data_Analysis_3_Vars/File_Paths/notebook_folder_path.txt', 'r').read()
# Running the notebooks
default_path = os.getcwd()
os.chdir('NBA_Data_Analysis_3_Vars')

notebooks = ['nba-experiment-baseline.ipynb', 'NBA-experiment.ipynb']

for notebook in notebooks:
    pm.execute_notebook(
        notebook,
        f'./{notebook_folder_path}/{notebook}'  # Das Notebook wird hier direkt überschrieben
    )
    
os.chdir(default_path)

# Calculate feature importance
calculate_feature_importance()

# Regression analysis
create_summary()