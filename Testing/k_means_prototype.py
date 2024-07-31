import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Daten aus CSV-Datei laden
data = pd.read_csv('/Users/sanaemessoudi/Desktop/Projekte/PAMI_Projekt9/Shift Explantion/00_simulate_data/Output Customer Data/customer_profile_0.csv')

# Diskrete und kontinuierliche Spalten definieren
discrete_columns = ['Connection', 'Unit_type', 'Day', 'Week']
continuous_columns = ['Weight']

# Diskrete Variablen mit One-Hot-Encoding umwandeln
data_one_hot = pd.get_dummies(data[discrete_columns])

# Kontinuierliche Variablen skalieren
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data[continuous_columns])

# Alle transformierten Daten zusammenfügen
data_preprocessed = np.concatenate([data_scaled, data_one_hot], axis=1)

# K-Means-Modell initialisieren und trainieren
kmeans = KMeans(n_clusters=22, random_state=42)
clusters = kmeans.fit_predict(data_preprocessed)

# Cluster-Zentren extrahieren und umkehren der Skalierung
cluster_centers = kmeans.cluster_centers_[:, :len(continuous_columns)]
cluster_centers_unscaled = scaler.inverse_transform(cluster_centers)

print(cluster_centers)
#print(cluster_centers_unscaled)

# Plotten der Daten
plt.scatter(data['Weight'], data['Day'], c=clusters, marker='o')

# Titel und Achsenbeschriftungen hinzufügen
plt.title('K-Means Clustering mit Ihren Daten')
plt.xlabel('Weight (continuous)')
plt.ylabel('Day (discrete)')

# Cluster-Zentren plotten
for center in cluster_centers_unscaled:
    plt.scatter(center[0], data['Day'].mean(), s=200, c='black', marker='X')

# Plot anzeigen
plt.show()
