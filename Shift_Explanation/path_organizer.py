import os
from dotenv import load_dotenv

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


folder_path_creation()