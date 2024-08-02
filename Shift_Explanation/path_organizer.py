import os
from dotenv import load_dotenv

# Pfad zur .env-Datei
dotenv_path = 'environment.env'  # Wenn die .env-Datei im selben Verzeichnis wie das Skript liegt

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv(dotenv_path)

# Zugriff auf die Umgebungsvariablen
path_root = os.getenv('OUTPUT_PATH_FOR_ANALYSIS')
folder_name = os.getenv('CURRENT_FOLDER_NAME')  # TODO: Please change this variable accordingly
path_customer_profiles = os.getenv('OUTPUT_CUSTOMER_PROFILES_PATHS')
path_distances = os.getenv('OUTPUT_DISTANCES')
path_shift_explanations = os.getenv('OUTPUT_SHIFT_EXPLANATIONS')
path_transport_graphics = os.getenv('OUTPUT_TRANSPORT_GRAPHICS')

# Create list of to-be-created folder paths
paths = [path_customer_profiles, path_distances, path_shift_explanations, path_transport_graphics]

# Beispiel für die Nutzung der Umgebungsvariablen
print(f'OUTPUT_PATH_FOR_ANALYSIS: {path_root}')

# Erstellen des Hauptordners
new_folder_path = os.path.join(path_root+folder_name)
print("Output Hauptordner:", new_folder_path)

# Sicherstellen, dass der Hauptordner existiert
os.makedirs(new_folder_path, exist_ok=False)

full_paths = []
# Erstellen der Unterordner
for path in paths:
    full_path = os.path.join(new_folder_path+path)
    print("Erstellen des Unterordners:", full_path)
    os.makedirs(full_path, exist_ok=False)
    full_paths.append(full_path)

path_customer_profiles = full_paths[0]
with open(path_root + "/File_Paths/path_customer_profiles.txt", "w") as f:
    f.write(path_customer_profiles)
path_distances = full_paths[1]
with open(path_root + "/File_Paths/path_distances.txt", "w") as f:
    f.write(path_distances)
path_shift_explanations = full_paths[2]
with open(path_root + "/File_Paths/path_shift_explanations.txt", "w") as f:
    f.write(path_shift_explanations)
path_transport_graphics = full_paths[3]
with open(path_root + "/File_Paths/path_transport_graphics.txt", "w") as f:
    f.write(path_transport_graphics)

print("#"*50)
print(path_customer_profiles)
