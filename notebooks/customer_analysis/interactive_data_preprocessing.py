import numpy as np
import pandas as pd
from z_data_utils import load_and_preprocess_adult_income_dataset

# hyperparamters
rng = np.random.RandomState(42)
n_samples = 1000
dataset_path = 'test_daten.csv'

raw_data = pd.read_csv(dataset_path, skipinitialspace=True)
column_names = list(raw_data.columns)

print("_______________________________________________________________________________________________")
print("Möchten Sie einige Attribute aus der Analyse entfernen?")
print(f"Folgende Attribute stehen zur Verfügung {column_names}.")
# Benutzer fragen, ob er einige Attribute entfernen möchte
remove_indices = input(f""">>> Geben Sie die Indexzahlen, getrennt durch Kommata, ein (z.B. 0,2,4): """)
print("_______________________________________________________________________________________________")

# Eingabe verarbeiten und Spalten entfernen
if remove_indices:
    try:
        # Indexzahlen in eine Liste umwandeln
        remove_indices = [int(idx) for idx in remove_indices.split(',')]

        # Zu entfernende Spaltennamen sammeln
        columns_to_remove = [column_names[idx] for idx in remove_indices]

        # Spalten aus dem DataFrame entfernen
        raw_data = raw_data.drop(columns=columns_to_remove)

        print()
        print("Aktualisiertes DataFrame:")
        print(raw_data.head(4))
    except (ValueError, IndexError) as e:
        print()
        print(f"Fehler bei der Verarbeitung der Eingabe: {e}")
else:
    print()
    print("Keine Attribute wurden entfernt.")
print("_______________________________________________________________________________________________")


# Find categorical variable
categorical_names = []
categorical_values = []
for col in raw_data.columns:
    unique_values = raw_data[col].dropna().unique().tolist()  # Eindeutige Werte ohne NaNs
    if 1 < len(unique_values) < 11:
        categorical_names.append(col)
        categorical_values.append(unique_values)

# Ask user which categorical attribute they would like to split the data on.
split_on_index = int(input(f">>> Please input the index of the attribute, you would like to split the data on {categorical_names}:"))
split_on = categorical_names[split_on_index]
print("_______________________________________________________________________________________________")

# Nur wenn Attribut nicht binär ist fragen, nach welchen zwei Kategorien aufgeteilt werden soll!
split_on_values = None
if raw_data[split_on].nunique() != 2:
    split_on_values = input(f">>> Which two categorical values would you like to compare for a distribution shift {categorical_values[split_on_index]}:")
    # Transform user input from string to list containing integers
    split_on_values = split_on_values.split(',')
    split_on_values = [int(value) for value in split_on_values]
print("_______________________________________________________________________________________________")

source, target, feature_names = load_and_preprocess_adult_income_dataset(split_on, raw_data, split_on_values,
                                                                         rng, n_samples, dataset_path,
                                                                         return_column_names=True)

