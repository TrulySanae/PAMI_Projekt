import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

# Load the dataset
df = pd.read_excel('/Users/sanaemessoudi/Desktop/Projekte/PAMI_Projekt9/notebooks/nba_analysis/real_datasets/NBA_Data.xlsx', sheet_name=1)
print(df)