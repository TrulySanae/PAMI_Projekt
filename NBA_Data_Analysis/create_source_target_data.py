import pandas as pd

# data_path = 'NBA_Data_Analysis/Data/NBA_Data_Datatype.csv'
data_path = 'NBA_Data_Analysis/Data/NBA_Data_Test.xlsx'
# nba_data = pd.read_csv(data_path, sep=";", encoding='latin1')
nba_data = pd.read_excel(data_path)

columns_to_keep = [
    "Team", "Age", "GamesPlayed", "Wins", "Losses", 
    "PointsScored", "FG%", "3P%", "FT%", "TotalRebounds", "Assists", 
    "Turnovers", "Steals", "Blocks", "PersonalFouls", "Year"
]

# Ensure the 'Year' column is of type integer
nba_data['Year'] = pd.to_numeric(nba_data['Year'], errors='coerce')

# Drop all other columns except the ones in columns_to_keep
nba_data = nba_data[columns_to_keep]
split_features = ['Team', 'Year']

# Define the feature the data will be split on
while True:
    print(f'Please enter the feature to split the data on:{split_features}')
    split_feature = input()
    print(f'Splitting the data on the feature: {split_feature}')
    if split_feature in split_features:
        break
    else:
        print(f'Feature {split_feature} not found in the data columns. Please try again.')
# Define the two instances of the feature to compare
if split_feature == 'Year':
    print('Please select the year to split the data on:')
    split_on_year = int(input())
    source_data = nba_data[nba_data['Year'] <= split_on_year]
    target_data = nba_data[nba_data['Year'] > split_on_year]  
    experiment_parameters = {'split_feature': split_feature, 'instance_1': f' YEAR <= {split_on_year}', 'instance_2': f' YEAR > {split_on_year}'}
else:
    while True:
        print(f'Please enter the first instance of the feature to compare:{nba_data[split_feature].unique()}')
        instance_1 = input()
        print(f'Please enter the second instance of the feature to compare:{nba_data[split_feature].unique()}')
        instance_2 = input()
        experiment_parameters = {'split_feature': split_feature, 'instance_1': instance_1, 'instance_2': instance_2}
        if instance_1 in nba_data[split_feature].unique() and instance_2 in nba_data[split_feature].unique():
            source_data = nba_data[nba_data[split_feature] == instance_1]
            target_data = nba_data[nba_data[split_feature] == instance_2]
            break
        else:
            print(f'Instances {instance_1} and {instance_2} not found in the data. Please try again.')

# Split the data based on the feature in source and target data
experiment_parameters = pd.DataFrame(experiment_parameters, index=[0])
experiment_parameters.to_csv(f'NBA_Data_Analysis/Source_Target/experiment_parameters_{experiment_parameters['instance_1'].values[0].replace(' ','')}_vs_{experiment_parameters['instance_2'].values[0].replace(' ','')}.csv', index=False)
source_data = source_data.drop(columns=['Team', 'Year'])
target_data = target_data.drop(columns=['Team', 'Year'])
print(f'Source data shape: {source_data.shape}, Target data shape: {target_data.shape}')
source_data.to_csv(f'NBA_Data_Analysis/Source_Target/source_data_{experiment_parameters['instance_1'].values[0].replace(' ','')}.csv', index=False)
target_data.to_csv(f'NBA_Data_Analysis/Source_Target/target_data_{experiment_parameters['instance_2'].values[0].replace(' ','')}.csv', index=False)