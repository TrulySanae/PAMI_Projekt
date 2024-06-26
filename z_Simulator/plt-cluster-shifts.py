import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
from utils import BaseTransport
import matplotlib.pyplot as plt

#import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from utils import BaseTransport

# Load the data
data_path = 'z_Simulator/test_daten.csv'
data = pd.read_csv(data_path)

# Standardize the features
features = ['Connection', 'Weight', 'Unit_type', 'Day']
scaler = StandardScaler()
data[features] = scaler.fit_transform(data[features])

# Initialize lists to track all transformations and significant customer changes
all_transformed_X = []
significant_changes = []

# Function to calculate the euclidean distance between two points
def euclidean_distance(a, b):
    return np.linalg.norm(a - b)

# Iterate over each pair of consecutive weeks
unique_weeks = sorted(data['Week'].unique())
for i in range(len(unique_weeks) - 1):
    week1 = unique_weeks[i]
    week2 = unique_weeks[i + 1]
    
    source_week = data[data['Week'] == week1]
    target_week = data[data['Week'] == week2]
    
    X_source = source_week[features].values
    X_target = target_week[features].values
    
    # Initialize and fit the BaseTransport model
    transport_model = BaseTransport(X_source, X_target, fit=True, alg='EMD')
    
    # Perform the forward transformation
    transformed_X = transport_model.forward(X_source)
    all_transformed_X.append(transformed_X)
    
    # Combine source data and transported data for paired clustering
    Z = np.hstack((X_source, transformed_X))
    
    # Apply k-means clustering
    k = 5  # Number of clusters, you can adjust this as needed
    kmeans = KMeans(n_clusters=k, random_state=0).fit(Z)
    
    # Extract paired source and target centroids
    mu_src = kmeans.cluster_centers_[:, :X_source.shape[1]]
    mu_tgt = kmeans.cluster_centers_[:, X_source.shape[1]:]
    
    # Define the final cluster-based map function
    def cluster_based_map(x, mu_src, mu_tgt):
        sigma = np.argmin(np.linalg.norm(x - mu_src, axis=1)**2)  # Cluster label function
        return x + (mu_tgt[sigma] - mu_src[sigma])
    
    # Apply the final transformation to the source data
    final_transformed_X = np.array([cluster_based_map(x, mu_src, mu_tgt) for x in X_source])
    
    # Identify customers with significant behavior changes
    threshold = 1.0  # Define a threshold for significant changes, adjust as needed
    for j in range(len(X_source)):
        if euclidean_distance(X_source[j], final_transformed_X[j]) > threshold:
            significant_changes.append((source_week.iloc[j]['Customer_id'], week1, week2))
    
    # Visualization
    plt.figure(figsize=(10, 6))
    plt.scatter(X_source[:, 1], X_source[:, 2], color='blue', label=f'Source Week {week1}')
    plt.scatter(final_transformed_X[:, 1], final_transformed_X[:, 2], color='red', label=f'Transformed Source Week {week1}')
    plt.scatter(X_target[:, 1], X_target[:, 2], color='green', label=f'Target Week {week2}')
    
    # Plot cluster centroids for visual aid
    plt.scatter(mu_src[:, 1], mu_src[:, 2], color='cyan', marker='x', s=100, label='Source Centroids')
    plt.scatter(mu_tgt[:, 1], mu_tgt[:, 2], color='magenta', marker='x', s=100, label='Target Centroids')
    
    plt.xlabel('Weight')
    plt.ylabel('Unit_type')
    plt.legend()
    plt.title(f'Cluster-Based Transport Analysis from Week {week1} to Week {week2}')
    plt.show()

# Summary of significant changes
significant_changes_df = pd.DataFrame(significant_changes, columns=['Customer_id', 'From_Week', 'To_Week'])
print("Significant Customer Behavior Changes:")
print(significant_changes_df)

# Further analysis and visualization can be added as needed
