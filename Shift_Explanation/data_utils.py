import numpy as np
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelBinarizer
from sklearn.utils import check_random_state




from sklearn.utils import check_random_state

def load_and_preprocess_logistics_data(random_state, max_samples=None, return_column_names=False, equal_week_split = True, comparison_id = 0, comparison_dict = None):
    rng = check_random_state(random_state)
    
    
    # Define file paths for dataset A and B
    path_customer_profiles = open('./Results_Experiments/File_Paths/path_customer_profiles.txt','r').read()
    file_path_a = f'../{path_customer_profiles}/customer_profile_{comparison_dict[comparison_id][0]}.csv'
    file_path_b = f'../{path_customer_profiles}/customer_profile_{comparison_dict[comparison_id][1]}.csv'
    print(file_path_a)
    print (f'Comparing customer_profile_{comparison_dict[comparison_id][0]} and customer_profile_{comparison_dict[comparison_id][1]}')
    
    # Load datasets
    data_a = pd.read_csv(file_path_a)
    data_b = pd.read_csv(file_path_b)

    source_data = data_a
    target_data = data_b
    
    if equal_week_split:
        # Determine the number of weeks
        weeks = source_data['Week'].unique()
        
        # Calculate samples per week needed
        if max_samples is not None:
            samples_per_week = max_samples // len(weeks)
        else:
            samples_per_week = min(source_data.shape[0], target_data.shape[0]) // len(weeks)

        # Sample data equally from each week
        sampled_source_data = pd.DataFrame()
        sampled_target_data = pd.DataFrame()

        for week in weeks:
            source_week_data = source_data[source_data['Week'] == week]
            target_week_data = target_data[target_data['Week'] == week]

            n_samples_week_source = min(samples_per_week, source_week_data.shape[0])
            n_samples_week_target = min(samples_per_week, target_week_data.shape[0])
            sampled_source_data = pd.concat([sampled_source_data, source_week_data.sample(n_samples_week_source, replace=False, random_state=rng)])
            sampled_target_data = pd.concat([sampled_target_data, target_week_data.sample(n_samples_week_target, replace=False, random_state=rng)])
    else:
        # Sample the datasets
        n_positive_samples = min(max_samples, source_data.shape[0]) if max_samples is not None else source_data.shape[0]
        source_data = source_data.sample(n_positive_samples, replace=False, random_state=rng)

        n_negative_samples = min(max_samples, target_data.shape[0]) if max_samples is not None else target_data.shape[0]
    # Drop columns that are not needed
    for df in [sampled_source_data, sampled_target_data]:
        df.drop(columns=['Day', 'Customer_id', 'Week'], inplace=True)
    
    # Convert to numpy arrays
    source = sampled_source_data.to_numpy().astype(float)
    target = sampled_target_data.to_numpy().astype(float)

    print(f'Finished preprocessing logistic dataset. Split on customer_profile_{comparison_dict[comparison_id][0]} and customer_profile_{comparison_dict[comparison_id][1]} with resulting source shape: {source.shape}, target shape: {target.shape}.')

    if return_column_names:
        return source, target, sampled_source_data.columns.to_list()
    else:
        return source, target