import papermill as pm
import os
import sys


import os
print(os.getcwd())
os.chdir('Shift_Explanation')
print(os.getcwd())

def execute_notebook_with_params(notebook_path, parameters, temp_output_path):
    pm.execute_notebook(
        notebook_path,
        temp_output_path,
        parameters=parameters
    )


# Parameter-Sätze definieren
parameter_sets = [
    {'comparison_id': 0,},
    {'comparison_id': 1},
    {'comparison_id': 2}
]

# Notebook-Pfad
notebook_path = 'adult-income-experiment.ipynb'
temp_output_path = notebook_path

# Notebook mit verschiedenen Parametern ausführen
for params in parameter_sets:
    execute_notebook_with_params(notebook_path, params, temp_output_path)