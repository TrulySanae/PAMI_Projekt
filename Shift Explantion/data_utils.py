import numpy as np
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelBinarizer
from sklearn.utils import check_random_state



# Adult income dataset
def load_and_preprocess_logistics_data(path_to_data_root, split_on_week,
                                             random_state=None, max_samples=None,
                                             return_column_names=False):
    rng = check_random_state(random_state)
    COLUMN_NAMES = ['Customer_id', 'Connection', 'Unit_type', 'Weight', 'Day', 'Week']
    raw_data = pd.read_csv('data_weightshift.csv')
    raw_data.drop(columns=['Day'], inplace=True)
  
    binary_variables = ['Connection', 'Unit_type']
    
    # def preprocess_data(raw_data, binary_variables):
    #     new_data = raw_data.copy()
    #     binarizer = LabelBinarizer(neg_label=0, pos_label=1)
    #     # Binarizing the binary_variables:
    #     for binary_var in binary_variables:
    #         new_data[binary_var] = binarizer.fit_transform(raw_data[binary_var])
    #     return new_data
    
    # processed_data = preprocess_data(raw_data, binary_variables)
    processed_data = raw_data.copy()
    split_on = split_on_week
    
   # Split the data based on split_on_week
    source_data = processed_data[processed_data['Week'] < split_on_week].drop(columns=['Week'])
    target_data = processed_data[processed_data['Week'] >= split_on_week].drop(columns=['Week'])
    
    if max_samples == 'balanced':
        # balance the two datasets
        max_samples = min(source_data.shape[0], target_data.shape[0])

    n_positive_samples = min(max_samples, source_data.shape[0]) if max_samples is not None else source_data.shape[0]
    source_data = source_data.sample(n_positive_samples, replace=False, random_state=rng)
    
    n_negative_samples = min(max_samples, target_data.shape[0]) if max_samples is not None else target_data.shape[0]
    target_data = target_data.sample(n_negative_samples, replace=False, random_state=rng)

    source = source_data.to_numpy().astype(float)  
    target = target_data.to_numpy().astype(float)  

    print(f'Finished preprocessing logistic dataset. ',
          f'Split on {split_on} with resulting source shape: {source.shape}, target shape: {target.shape}.')
    if return_column_names:
        return source, target, source_data.columns.to_list()
    else:
        return source, target