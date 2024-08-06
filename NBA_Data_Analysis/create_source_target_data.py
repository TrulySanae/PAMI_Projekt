import pandas as pd

data_path = 'NBA_Data_Analysis/Data/NBA_Data.xlsx'
nba_data = pd.read_excel(data_path)


data_columns = nba_data.columns

def create_source_target_data_interactive(nba_data):
    data_columns = nba_data.columns
    # # drop columns that are not needed
    # while True:
    #     print(f'Please enter the columns to drop:{data_columns}')
    #     columns_to_drop = input()
    #     print(f'Dropping the columns: {columns_to_drop}')
    #     if columns_to_drop in data_columns:
    #         break
    #     else:
    #         print(f'Columns {columns_to_drop} not found in the data columns. Please try again.')
    # Define the feature the data will be split on
    while True:
        print(f'Please enter the feature to split the data on:{data_columns}')
        split_feature = input()
        print(f'Splitting the data on the feature: {split_feature}')
        if split_feature in data_columns:
            break
        else:
            print(f'Feature {split_feature} not found in the data columns. Please try again.')
    # Define the two instances of the feature to compare
    if split_feature == 'year':
        print('Please select the year to split the data on:')
        split_on_year = input()
        source_data = nba_data[nba_data['year'] <= split_on_year]
        target_data = nba_data[nba_data['year'] > split_on_year]
        print(f'Source data shape: {source_data.shape}, Target data shape: {target_data.shape}')
        source_data.to_csv('NBA_Data_Analysis/Source_Target/source_data.csv', index=False)
        target_data.to_csv('NBA_Data_Analysis/Source_Target/target_data.csv', index=False)
        experiment_parameters = {'split_feature': split_feature, 'instance_1': f' YEAR <= {split_on_year}', instance_2: f' YEAR > {split_on_year}'}
    while True:
        print(f'Please enter the first instance of the feature to compare:{nba_data[split_feature].unique()}')
        instance_1 = input()
        print(f'Please enter the second instance of the feature to compare:{nba_data[split_feature].unique()}')
        instance_2 = input()
        if instance_1 in nba_data[split_feature].unique() and instance_2 in nba_data[split_feature].unique():
            break
        else:
            print(f'Instances {instance_1} and {instance_2} not found in the data. Please try again.')

    # Split the data based on the feature in source and target data

    source_data = nba_data[nba_data[split_feature] == instance_1]
    target_data = nba_data[nba_data[split_feature] == instance_2]
    experiment_parameters = {'split_feature': split_feature, 'instance_1': instance_1, 'instance_2': instance_2}
    experiment_parameters = pd.DataFrame(experiment_parameters, index=[0])
    experiment_parameters.to_csv('NBA_Data_Analysis/Source_Target/experiment_parameters.csv', index=False)
    print(f'Source data shape: {source_data.shape}, Target data shape: {target_data.shape}')
    source_data.to_csv('NBA_Data_Analysis/Source_Target/source_data.csv', index=False)
    target_data.to_csv('NBA_Data_Analysis/Source_Target/target_data.csv', index=False)

create_source_target_data_interactive(nba_data)