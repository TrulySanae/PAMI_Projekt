import os
import papermill as pm
from pathlib import Path
from dotenv import load_dotenv

folders = [
    "Baseline",
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
path_root = "Shift_Explanation/Results_Experiments"
default_path = os.getcwd()
print('#'*50)
print(default_path)



for folder_name in folders:
    os.chdir(default_path)
    print(os.getcwd())
   
    folder_name = f'/{folder_name}'
    path_customer_profiles = os.path.join(path_root + folder_name + '/Customer_Profiles')
    path_distances = os.path.join(path_root + folder_name + '/Distances')
    path_shift_explanations = os.path.join(path_root + folder_name + '/Shift_Explanation')
    path_transport_graphics = os.path.join(path_root + folder_name + '/Transport_Graphic')
    notebook_folder_path = f'Results_Experiments{folder_name}'
    with open(path_root + "/File_Paths/path_customer_profiles.txt", "w") as f:
        f.write(path_customer_profiles)
    with open(path_root + "/File_Paths/path_distances.txt", "w") as f:
        f.write(path_distances)
    with open(path_root + "/File_Paths/path_shift_explanations.txt", "w") as f:
        f.write(path_shift_explanations)
    with open(path_root + "/File_Paths/path_transport_graphics.txt", "w") as f:
        f.write(path_transport_graphics)
    with open(path_root + "/File_Paths/notebook_folder_path.txt", "w") as f:
        f.write(notebook_folder_path)
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

    notebooks = ['experiment_baseline', 'k_Means_cluster_transport']
    

    for notebook in notebooks:
        for i, params in enumerate(parameter_sets, start=1):
            
            # Füge dem Dateinamen einen Zähler hinzu
            output_path = f'./{notebook_folder_path}/{notebook}_{i}.ipynb'
            # if os.path.exists(output_path):
            #     continue
            print(output_path)
            execute_notebook_with_params(f'{notebook}.ipynb', params, output_path)

    