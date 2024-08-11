import path_organizer
import os
import papermill as pm
from pathlib import Path

folders = [
    "Set_C_max_to_10",
    "Set_C_max_to_60",
    "Set_C_max_to_None_Set_V_max_to_None_Set_lambd_to_None_Set_UT_list_to_None_Set_weight_span_to_None_Set_num_components_to_None_Set_number_of_connections_to_None",
    "Set_K_to_30",
    "Set_K_to_100",
    "Set_lambd_to_0.01",
    "Set_lambd_to_0.12",
    "Set_num_components_to_1",
    "Set_num_components_to_6",
    "Set_number_of_connections_to_2",
    "Set_number_of_connections_to_10",
    "Set_number_of_connections_to_None",
    "Set_sim_weeks_to_2",
    "Set_sim_weeks_to_10",
    "Set_UT_list_to_None",
    "Set_UT_list_to_None_Set_weight_span_to_None_Set_num_components_to_None_Set_number_of_connections_to_2",
    "Set_UT_list_to_None_Set_weight_span_to_None_Set_num_components_to_None_Set_number_of_connections_to_None",
    "Set_V_max_to_15",
    "Set_V_max_to_90",
    "Set_weight_span_to_None"
]

default_path = os.getcwd()


for folder_name in folders:
    # Write a new environment variable
    env_var_value = f'/{folder_name}'  # Anführungszeichen entfernt
    env_var_name = "CURRENT_FOLDER_NAME"
    env_path = Path('environment.env')
    env_path.touch(exist_ok=True)
    lines = env_path.read_text().splitlines()
    new_lines = [line for line in lines if not line.startswith(f"{env_var_name}=")]
    new_lines.append(f"{env_var_name}={env_var_value}")
    env_path.write_text("\n".join(new_lines) + "\n")
    print(f"Set {env_var_name}={env_var_value} in {env_path}")
    # Führe die Funktion folder_path_creation aus
    path_organizer.folder_path_creation()
    
    # Processing the data to get distances and Transportcosts
    notebook_folder_path = open('Shift_Explanation/Results_Experiments/File_Paths/notebook_folder_path.txt', 'r').read()  
   
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

    notebook_path = 'k_Means_cluster_transport.ipynb'
    

    for i, params in enumerate(parameter_sets, start=1):
        
        # Füge dem Dateinamen einen Zähler hinzu
        output_path = f'./{notebook_folder_path}/k_Means_cluster_transport_{i}.ipynb'
        if os.path.exists(output_path):
            pass
        print(output_path)
        execute_notebook_with_params(notebook_path, params, output_path)

    os.chdir(default_path)