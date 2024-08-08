import pandas as pd
from sklearn.utils import check_random_state

# Function to load and preprocess logistics data
def load_and_preprocess_nba_data(parameters_path, random_state=None, max_samples=None, return_column_names=False):
    rng = check_random_state(random_state)

    # Define file paths for dataset
    file_path_a = './Source_Target/source_data_YEAR<=2009.csv'  # Adjust this path to your first CSV file location
    file_path_b = './Source_Target/target_data_YEAR>2009.csv'  # Adjust this path to your second CSV file location
    file_path_c = parameters_path

    source_data = pd.read_csv(file_path_a)
    target_data = pd.read_csv(file_path_b)
    parameters = pd.read_csv(file_path_c)


    # Ensure both datasets have the same number of rows
    n_samples = min(source_data.shape[0], target_data.shape[0])

    source_data = source_data.sample(n_samples, replace=False, random_state=rng)
    target_data = target_data.sample(n_samples, replace=False, random_state=rng)

    # Convert to numpy arrays
    source = source_data.to_numpy().astype(float)
    target = target_data.to_numpy().astype(float)

    print(f'Splitting on {parameters['split_feature'].values[0]} with {parameters['instance_1'].values[0]} and {parameters['instance_2'].values[0]} resulting source shape: {source.shape}, target shape: {target.shape}.')

    print("###############################")
    print(source_data.columns.to_list())
    print("###############################")

    print("######################## Source_Data_A Dropped ##########################")
    print(source_data)
    print("########################### Source_Data_B Dropped #######################")
    print(target_data)
    print("##################################################")

    if return_column_names:
        return source, target, source_data.columns.to_list()
    else:
        return source, target


