import pandas as pd
import os
# data_path = 'NBA_Data_Analysis/Data/NBA_Data_Datatype.csv'


def get_source_target_data(nba_data):
    columns_to_keep = [
        "Team", "Age", "GamesPlayed", 'MinutesPlayed' , 
        "PointsScored",'NetScoreOfPlayer', "Year"
    ]

    # Ensure the 'Year' column is of type integer
    nba_data['Year'] = pd.to_numeric(nba_data['Year'], errors='coerce')

    # Drop all other columns except the ones in columns_to_keep
    nba_data = nba_data[columns_to_keep]
    split_features = ['Team', 'Year']
    independent_vars1 = {'1':'PointsScored', '2':'NetScoreOfPlayer'}
    independent_vars2 = {'1':'GamesPlayed', '2':'MinutesPlayed'}
    # Define the feature the data will be split on
    print(f'Please select the independent variable you prefer:{independent_vars1}')
    independent_var1 = independent_vars1[input()]
    print(f'Please select the independent variable you prefer:{independent_vars2}')
    independent_var2 = independent_vars2[input()]
    independent_vars1_drop = [x for x in independent_vars1.values() if x != independent_var1]
    independent_vars2_drop = [x for x in independent_vars2.values() if x != independent_var2]

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
        experiment_parameters = {'split_feature': split_feature, 'instance_1': f' YEAR <= {split_on_year}', 'instance_2': f' YEAR > {split_on_year}','independent_var1':independent_var1,'independent_var2':independent_var2}
    else:
        while True:
            print(f'Please enter the first instance of the feature to compare:{nba_data[split_feature].unique()}')
            instance_1 = input()
            print(f'Please enter the second instance of the feature to compare:{nba_data[split_feature].unique()}')
            instance_2 = input()
            experiment_parameters = {'split_feature': split_feature, 'instance_1': instance_1, 'instance_2': instance_2,'independent_var1':independent_var1,'independent_var2':independent_var2}
            if instance_1 in nba_data[split_feature].unique() and instance_2 in nba_data[split_feature].unique():
                source_data = nba_data[nba_data[split_feature] == instance_1]
                target_data = nba_data[nba_data[split_feature] == instance_2]
                break
            else:
                print(f'Instances {instance_1} and {instance_2} not found in the data. Please try again.')
    return source_data, target_data, experiment_parameters, independent_vars1_drop, independent_vars2_drop
# Split the data based on the feature in source and target data

def create_folders(experiment_parameters):
    main_folder_path = f'NBA_Data_Analysis_3_Vars/{experiment_parameters['instance_1'].replace(' ','')}_vs_{experiment_parameters['instance_2'].replace(' ','')}_{experiment_parameters['independent_var1']}_{experiment_parameters['independent_var2']}'
    print(main_folder_path)
    folders_list = ['/Source_Target', '/Results_Experiments']
    results_folders = ['/Distance','/Baseline_Meanshift','/Regression']
    results_paths = []
    for folder in results_folders:
        path = os.path.join(main_folder_path + '/Results_Experiments' + folder)
        results_paths.append(path)
    print(results_paths)
    try:
        os.makedirs(main_folder_path, exist_ok=False)
    except: # Falls der Ordner bereits existiert
        print("Der Ordner existiert bereits")
    for folder in folders_list:
        try:
            os.makedirs(main_folder_path+folder, exist_ok=False)
        except: # Falls der Ordner bereits existiert
            print("Der Ordner existiert bereits")
    for path in results_paths:
        try:
            os.makedirs(path, exist_ok=False)
        except: # Falls der Ordner bereits existiert
                print("Der Ordner existiert bereits")
    path_source_target = os.path.join(main_folder_path + folders_list[0])
    path_distances = results_paths[0]
    path_baseline = results_paths[1]
    path_regression = results_paths[2]
    return path_source_target, path_distances, path_baseline, path_regression


def write_file_paths(path_source_target, path_distances, path_baseline, path_regression):
    with open('NBA_Data_Analysis_3_Vars/File_Paths/path_source_target.txt', 'w') as f:
        f.write(path_source_target)
    with open('NBA_Data_Analysis_3_Vars/File_Paths/path_distances.txt', 'w') as f:
        f.write(path_distances)
    with open('NBA_Data_Analysis_3_Vars/File_Paths/path_baseline.txt', 'w') as f:
        f.write(path_baseline)
    with open('NBA_Data_Analysis_3_Vars/File_Paths/path_regression.txt', 'w') as f:
        f.write(path_regression)

def create_source_target_data(experiment_parameters, source_data, target_data, path_source_target,independent_vars1_drop,independent_vars2_drop):
    experiment_parameters = pd.DataFrame(experiment_parameters, index=[0])
    experiment_parameters.to_csv(f'{path_source_target}/experiment_parameters.csv', index=False)
    source_data = source_data.drop(columns=['Team', 'Year', independent_vars1_drop[0], independent_vars2_drop[0]])
    target_data = target_data.drop(columns=['Team', 'Year', independent_vars1_drop[0], independent_vars2_drop[0]])
    print(f'Source data shape: {source_data.shape}, Target data shape: {target_data.shape}')
    source_data.to_csv(f'{path_source_target}/source_data_{experiment_parameters['instance_1'].values[0].replace(' ','')}.csv', index=False)
    target_data.to_csv(f'{path_source_target}/target_data_{experiment_parameters['instance_2'].values[0].replace(' ','')}.csv', index=False)
 
def create_all_data():
    data_path = 'NBA_Data_Analysis_3_Vars/Data/NBA_Data_Test.xlsx'
    nba_data = pd.read_excel(data_path)
    source_data, target_data, experiment_parameters, independent_vars1_drop, independent_vars2_drop = get_source_target_data(nba_data)
    path_source_target, path_distances, path_baseline, path_regression = create_folders(experiment_parameters)
    write_file_paths(path_source_target, path_distances, path_baseline, path_regression) 
    create_source_target_data(experiment_parameters, source_data, target_data, path_source_target, independent_vars1_drop, independent_vars2_drop)  

#create_all_data()