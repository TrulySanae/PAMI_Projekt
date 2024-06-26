from utils import BaseTransport
from data_gen_utils import data_split
import pandas as pd
from kmodes.kprototypes import KPrototypes

file_path = 'z_Simulator/test_daten.csv'
logistic_data = pd.read_csv(file_path) 
feature_names = logistic_data.columns
X, Y = data_split(logistic_data)
Y = Y[Y['Week'] == 2]

continuous_variables_indicies = [2]
if X.shape[0] > Y.shape[0]:
    X.drop(X.tail(X.shape[0] - Y.shape[0]).index, inplace=True)
elif Y.shape[0] > X.shape[0]:
    Y.drop(Y.tail(Y.shape[0] - X.shape[0]).index, inplace=True)

X = X.to_numpy()
Y = Y.to_numpy()

# Diskrete und kontinuierliche Spalten identifizieren
categorical_columns = ['Customer_id','Connection', 'Unit_type', 'Day']
continuous_columns = ['Weight']

# Funktion zur Kodierung der kategorischen Daten und Clustering
def process_weekly_clustering(logistic_data, week, n_clusters):
    df_week = logistic_data[logistic_data['Week'] == week].copy()
    
    # Umwandeln der kategorischen Spalten mit Label-Encoding
    for column in categorical_columns:
        df_week[column] = df_week[column].astype('category')
        df_week[column] = df_week[column].cat.codes
    
    # Konvertiere den DataFrame in ein NumPy-Array
    data_matrix = df_week.drop(['Week'], axis=1).to_numpy()
    
    # K-Prototypen Clustering
    kproto = KPrototypes(n_clusters=n_clusters, init='Huang', random_state=42)
    clusters = kproto.fit_predict(data_matrix, categorical=[0, 1, 2])
    
    # Ergebnisse zum DataFrame hinzufügen
    df_week['Cluster'] = clusters
    
    # Durchschnittswerte der kontinuierlichen Merkmale pro Cluster
    mean_values = df_week.groupby('Cluster')[continuous_columns].mean()
    
    # Moden der diskreten Merkmale pro Cluster
    mode_values = df_week.groupby('Cluster')[categorical_columns].agg(lambda x: x.mode()[0])
    
    # Rückkodierung der diskreten Merkmale
    for column in categorical_columns:
        mapping = dict(enumerate(logistic_data[logistic_data['Week'] == week][column].astype('category').cat.categories))
        mode_values[column] = mode_values[column].map(mapping)
    
    # Zusammenführen der Durchschnittswerte und Moden
    cluster_summary = pd.concat([mean_values, mode_values], axis=1)
    
    return cluster_summary

# Clusterbildung und Berechnung der Durchschnittswerte für jede Woche
weeks = logistic_data['Week'].unique()
weekly_cluster_summaries = {}

for week in weeks:
    cluster_summary = process_weekly_clustering(logistic_data, week, n_clusters=10)
    weekly_cluster_summaries[week] = cluster_summary
    print(f"Cluster-Durchschnittswerte für Woche {week}:")
    print(cluster_summary)
    print("\n")

# Optional: Kombiniere alle Wochenergebnisse in einem DataFrame
combined_summary = pd.concat(weekly_cluster_summaries, axis=0)
combined_summary.index.names = ['Week', 'Cluster']

print("Kombinierte Cluster-Durchschnittswerte:")
print(combined_summary)
# print(X.shape, Y.shape)


# T = BaseTransport(X, Y, fit=True)

# Z = T.forward(X,Y)

# # Create a Dataframe to compare the original and transformed data side by side

# logistic_data = pd.DataFrame(data=X, columns=feature_names)