import os
import papermill as pm
from pathlib import Path
from dotenv import load_dotenv

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
print('#'*50)
print(default_path)

def folder_path_creation():
    # Pfad zur .env-Datei
    dotenv_path = 'environment.env'  # Wenn die .env-Datei im selben Verzeichnis wie das Skript liegt

    # Laden der Umgebungsvariablen aus der .env-Datei
    load_dotenv(dotenv_path)

    # Zugriff auf die Umgebungsvariablen
    path_root = os.getenv('OUTPUT_PATH_FOR_ANALYSIS')
    folder_name = os.getenv('CURRENT_FOLDER_NAME')
    path_customer_profiles = os.getenv('OUTPUT_CUSTOMER_PROFILES_PATHS')
    path_distances = os.getenv('OUTPUT_DISTANCES')
    path_shift_explanations = os.getenv('OUTPUT_SHIFT_EXPLANATIONS')
    path_transport_graphics = os.getenv('OUTPUT_TRANSPORT_GRAPHICS')
    print('#'*50)
    print(folder_name)
    # Create list of to-be-created folder paths
    paths = [path_customer_profiles, path_distances, path_shift_explanations, path_transport_graphics]


    # Erstellen des Hauptordners
    new_folder_path = os.path.join(path_root+folder_name)
    print("Output Hauptordner:", new_folder_path)

    # Sicherstellen, dass der Hauptordner existiert
    try:
        os.makedirs(new_folder_path, exist_ok=False)
    except: # Falls der Ordner bereits existiert
        print("Der Ordner existiert bereits")

    full_paths = []
    # Erstellen der Unterordner
    for path in paths:
        full_path = os.path.join(new_folder_path+path)
        try:
            os.makedirs(full_path, exist_ok=False)
        except: # Falls der Ordner bereits existiert
            print("Der Ordner existiert bereits")
        full_paths.append(full_path)

    # Speichern der Pfade in Textdateien

    path_customer_profiles = full_paths[0]
    path_distances = full_paths[1]
    path_shift_explanations = full_paths[2]
    path_transport_graphics = full_paths[3]
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

for folder_name in folders:
    os.chdir(default_path)
    print(os.getcwd())
    # Write a new environment variable
    env_var_value = f'"/{folder_name}"'  # Anführungszeichen entfernt
    env_var_name = "CURRENT_FOLDER_NAME"
    env_path = Path('environment.env')
    env_path.touch(exist_ok=True)
    lines = env_path.read_text().splitlines()
    new_lines = [line for line in lines if not line.startswith(f"{env_var_name}=")]
    new_lines.append(f"{env_var_name}={env_var_value}")
    env_path.write_text("\n".join(new_lines) + "\n")
    print(f"Set {env_var_name}={env_var_value} in {env_path}")
    # Führe die Funktion folder_path_creation aus
    folder_path_creation()
    
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
            continue
        print(output_path)
        execute_notebook_with_params(notebook_path, params, output_path)

    