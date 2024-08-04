import papermill as pm
from pathlib import Path
import os
from simulate_data.simulating_shifts import datasets_creation
from path_organizer import folder_path_creation
from analyse_results import create_summary

# TODO: Set the new folder name
env_var_value = '"/Test"' 

# TODO: Choose fixe parameters to create datasets
K = None
sim_weeks = None
C_max = None
V_max = None
lambd = None
UT_list = None
weight_span = None
num_components = None
number_of_connections = None
num_profiles = None #Default is 6

# Write a new environment variable
env_var_name = "CURRENT_FOLDER_NAME"
env_path = Path('environment.env')
env_path.touch(exist_ok=True)
lines = env_path.read_text().splitlines()
new_lines = [line for line in lines if not line.startswith(f"{env_var_name}=")]
new_lines.append(f"{env_var_name}={env_var_value}")
env_path.write_text("\n".join(new_lines) + "\n")
print(f"Set {env_var_name}={env_var_value} in {env_path}")

# Create new result folders 
folder_path_creation()

# Create datasets
datasets_creation(C_max, V_max, lambd, UT_list, weight_span, num_components, number_of_connections, K, sim_weeks, num_profiles)


# Processing the data to get distances and Transportcosts
os.chdir('Shift_Explanation')
print(os.getcwd())

def execute_notebook_with_params(notebook_path, parameters, output_path):
    pm.execute_notebook(
        notebook_path,
        output_path,
        parameters=parameters
    )
parameter_sets = [
    {'comparison_id': 0,},
    {'comparison_id': 1},
    {'comparison_id': 2}
]
notebook_path = 'adult-income-experiment.ipynb'
output_path = notebook_path
for params in parameter_sets:
    execute_notebook_with_params(notebook_path, params, output_path)

# Create summary
create_summary()