from Transport_Mapping import Z, Z_continuous, T
from preprocessing import X, Y, rng
import numpy as np
from sklearn.preprocessing import StandardScaler
from explainability_measures import get_mixed_variable_desiderata


continuous_variables_indicies = [0,1,2]
max_clusters = 10

standardizer = StandardScaler()
standardizer = standardizer.fit(X)
X_continuous, Y_continuous = standardizer.transform(X), standardizer.transform(Y)

cluster_histories = []

# Empty numpy arrays for storing explain ability measures
fids = np.zeros(max_clusters+1)
pars = np.zeros(max_clusters+1)
inters = np.zeros(max_clusters+1)

# Calculate clusters and
for n_clusters in range(1, max_clusters+1):
    # performs paired clustering in a continuous joint X,Z space
    cluster_labels = T._pair_clustering(X_continuous, Z=Z_continuous, n_clusters=n_clusters, rng=rng)
    # print("cluster_lables:", cluster_labels)

    Z_clusters = np.zeros_like(Z)  # the final output of the cluster mean shift transport
    for cluster_idx in range(n_clusters):
        X_cluster = X[cluster_labels == cluster_idx]
        Z_cluster = Z[cluster_labels == cluster_idx]
    # print("X_cluster:", X_cluster)
    # print("Z_cluster:", Z_cluster)

    # TODO: Below here only calculation of explain ability measures
    # getting desiderata information
    fid, par, inter = get_mixed_variable_desiderata(X_continuous, Y_continuous, Z_clusters, standardizer,
                                                    continuous_variables_indicies, n_expectation=30,
                                                    inter=n_clusters, rng=rng)
    fids[n_clusters] = fid
    pars[n_clusters] = par
    inters[n_clusters] = n_clusters

    cluster_record = {
        'labels': cluster_labels.copy(),
        'Z_clusters': Z_clusters.copy(),
        'n_clusters': n_clusters
    }
    cluster_histories.append(cluster_record)