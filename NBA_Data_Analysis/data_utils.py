import pandas as pd
from sklearn.utils import check_random_state

# Function to load and preprocess logistics data
def load_and_preprocess_logistics_data(random_state=None, max_samples=None, return_column_names=False):
    rng = check_random_state(random_state)

    # Define file paths for dataset
    file_path = '/Users/sanaemessoudi/Desktop/Projekte/PAMI_Projekt9/NBA_Data_Analysis/NBA_Data.xlsx'

    # Load dataset
    data = pd.read_excel(file_path, sheet_name=1)

    # Correctly filter data based on TEAM and Year
    # source_data = data[(data["Team"] == "LAL") & (data["Year"] == 2023)].copy()
    # target_data = data[(data["Team"] == "CLE") & (data["Year"] == 2023)].copy()

    source_data = data[(data["Team"] == "LAL")].copy()
    target_data = data[(data["Team"] == "CLE")].copy()

    print("######################## Source_Data_A ##########################")
    print(source_data)
    print("########################### Source_Data_B #######################")
    print(target_data)
    print("##################################################")

    # Drop columns that are not needed
    columns_to_drop = ['MinutesPlayed', 'PointsScored', 'FieldGoalsMade', 'FieldGoalsAttempted',
                       'ThreePointFieldGoalsMade', 'ThreePointFieldGoalsAttempted', 'FreeThrowsMade',
                       'FreeThrowsAttempted', 'OffensiveRebounds', 'DefensiveRebounds', 'FantasyPoints',
                       'DoubleDoubles', 'TripleDoubles', 'Player', 'Team', 'Year']

    for df in [source_data, target_data]:
        df.drop(columns=columns_to_drop, inplace=True)

    # Ensure both datasets have the same number of rows
    n_samples = min(source_data.shape[0], target_data.shape[0])

    source_data = source_data.sample(n_samples, replace=False, random_state=rng)
    target_data = target_data.sample(n_samples, replace=False, random_state=rng)

    # Convert to numpy arrays
    source = source_data.to_numpy().astype(float)
    target = target_data.to_numpy().astype(float)

    print(f'Finished preprocessing logistic dataset. ',
          f'Split on Data A and Data B with resulting source shape: {source.shape}, target shape: {target.shape}.')

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

# Call the function (example)
source, target = load_and_preprocess_logistics_data()
