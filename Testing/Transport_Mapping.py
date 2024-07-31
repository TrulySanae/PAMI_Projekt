import numpy as np
import pandas as pd
from utils import BaseTransport
from data_utils import load_and_preprocess_logistics_data
from sklearn.preprocessing import StandardScaler
from preprocessing import X, Y

# fitting standardizer on our source domain
standardizer = StandardScaler()
standardizer = standardizer.fit(X)
T = BaseTransport(X, Y, fit=True)
Z = T.forward(X, Y)
Z_continuous = standardizer.transform(Z)
data_z = pd.DataFrame(Z)
data_z_cont = pd.DataFrame(Z_continuous)
print("##################################################")
print("##################################################")
print("########################Transformiert##########################")
print(data_z)
print("#############################Kontinuierlich Transformiert#####################")
print(data_z_cont)




