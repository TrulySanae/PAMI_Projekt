import numpy as np
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelBinarizer
from sklearn.utils import check_random_state



# Adult income dataset
import pandas as pd
from sklearn.utils import check_random_state

def load_and_preprocess_logistics_data(path_to_data_root,
                                        random_state=None, max_samples=None,
                                        return_column_names=False):
    rng = check_random_state(random_state)
    
    # Define file paths for dataset A and B
    file_path_a = f'./00_simulate_data/Output Customer Data/customer_profile_0.csv'
    file_path_b = f'./00_simulate_data/Output Customer Data/customer_profile_1.csv'

    # Load datasets
    data_a = pd.read_csv(file_path_a)
    data_b = pd.read_csv(file_path_b)

    # Load datasets
    data_a = pd.read_csv(file_path_a)
    data_b = pd.read_csv(file_path_b)

    source_data = data_a[data_a["Customer_id"] == 1]
    target_data = data_b[data_b["Customer_id"] == 1]

    print("########################Source_Data_A##########################")
    print(source_data)
    print("###########################Source_Data_B#######################")
    print(target_data)
    print("##################################################")
    print("##################################################")
    print("##################################################")

    if max_samples == 'balanced':
        # Balance the two datasets
        max_samples = min(source_data.shape[0], target_data.shape[0])

    # Sample the datasets
    n_positive_samples = min(max_samples, source_data.shape[0]) if max_samples is not None else source_data.shape[0]
    source_data = source_data.sample(n_positive_samples, replace=False, random_state=rng)

    n_negative_samples = min(max_samples, target_data.shape[0]) if max_samples is not None else target_data.shape[0]
    target_data = target_data.sample(n_negative_samples, replace=False, random_state=rng)

    # Drop columns that are not needed
    for df in [source_data, target_data]:
        df.drop(columns=['Day', 'Customer_id', 'Week'], inplace=True)

    # Convert to numpy arrays
    source = source_data.to_numpy().astype(float)
    target = target_data.to_numpy().astype(float)

    print(f'Finished preprocessing logistic dataset. ',
          f'Split on Data A and Data with resulting source shape: {source.shape}, target shape: {target.shape}.')

    print("###############################")
    print(source_data.columns.to_list())
    print("###############################")

    print("########################Source_Data_A Droped##########################")
    print(source_data)
    print("###########################Source_Data_B Droped#######################")
    print(target_data)
    print("##################################################")
    print("##################################################")
    print("##################################################")

    if return_column_names:
        return source, target, source_data.columns.to_list()
    else:
        return source, target