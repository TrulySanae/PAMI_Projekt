import papermill as pm
import os

# Setting up the correct working directory

os.chdir('Shift_Explanation')
print(os.getcwd())

def execute_notebook_with_params(notebook_path, parameters, output_path):
    pm.execute_notebook(
        notebook_path,
        output_path,
        parameters=parameters
    )


# define the parameters for the notebook
parameter_sets = [
    {'comparison_id': 0,},
    {'comparison_id': 1},
    {'comparison_id': 2}
]

# Notebook path
notebook_path = 'adult-income-experiment.ipynb'
output_path = notebook_path

# Running the notebook with the 3 dataset pairs
for params in parameter_sets:
    execute_notebook_with_params(notebook_path, params, output_path)