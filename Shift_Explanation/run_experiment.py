import papermill as pm
from pathlib import Path
import os
from simulate_data.simulating_shifts import datasets_creation
from path_organizer import folder_path_creation
from analyse_results import create_summary
from results_comparison import compare_results

# TODO: Set the new folder name
env_var_value = '"/Test"' 

# TODO: Choose fixe parameters to create datasets
print("#"*50)
chosen_simulation_parameters = {
"K": 50,
    "sim_weeks": 6,
    "C_max": 20,
    "V_max": 50,
    "lambd": 0.1,
    "UT_list": [20, 20, 20, 20, 20, 20],
    "weight_span": None,
    "num_components": 3,
    "number_of_connections": 5,
    "num_profiles": 6, #Default is 6
    
}

baseline = {
    "K": 50,
    "sim_weeks": 6,
    "C_max": 20,
    "V_max": 50,
    "lambd": 0.1,
    "UT_list": [20, 20, 20, 20, 20, 20],
    "weight_span": [3, 40],
    "num_components": 3,
    "number_of_connections": 5,
    "num_profiles": 6, #Default is 6
}
print("#"*50)

# Find changed parameters
changed_parameters = {key: chosen_simulation_parameters[key] for key in chosen_simulation_parameters if chosen_simulation_parameters[key] != baseline.get(key)}
# Create the string with changed parameters
if changed_parameters:
    changed_parameters_str = '_'.join([f"Set_{key}_to_{value}" for key, value in changed_parameters.items()])
else:
    changed_parameters_str = "Baseline"
# Set the new folder name
env_var_value = f'"/{changed_parameters_str}"'
print(env_var_value)

print("#"*50)

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

# Extracting values from the dictionary
C_max = chosen_simulation_parameters['C_max']
V_max = chosen_simulation_parameters['V_max']
lambd = chosen_simulation_parameters['lambd']
UT_list = chosen_simulation_parameters['UT_list']
weight_span = chosen_simulation_parameters['weight_span']
num_components = chosen_simulation_parameters['num_components']
number_of_connections = chosen_simulation_parameters['number_of_connections']
K = chosen_simulation_parameters['K']
sim_weeks = chosen_simulation_parameters['sim_weeks']
num_profiles = chosen_simulation_parameters['num_profiles']

# Create datasets
datasets_creation(C_max, V_max, lambd, UT_list, weight_span, num_components, number_of_connections, K, sim_weeks, num_profiles)


# Processing the data to get distances and Transportcosts
default_path = os.getcwd()
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

os.chdir(default_path)

# Create summary
create_summary()

# Create new comparison summary to baseline
compare_results()