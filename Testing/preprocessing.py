from data_utils import load_and_preprocess_logistics_data
import numpy as np
import pandas as pd

rng = np.random.RandomState(42)
# n_samples = 'balanced'
n_samples = 1000


X, Y, feature_names = load_and_preprocess_logistics_data(rng, n_samples, return_column_names=True)
print("##################################################")
print("##################################################")
print("########################Input Daten X und Y fürs Mapping##########################")
data_X = pd.DataFrame(X)
print("#########################X-Daten########################")
print(data_X)
print("########################Y-Daten##########################")
data_Y = pd.DataFrame(Y)
print(data_Y)
print("##########################Attributnamen########################")
print("feature names:", feature_names)