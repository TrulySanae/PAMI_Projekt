import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

def calculate_feature_importance():
    # Load the CSV file
    path_distances = open('./NBA_Data_Analysis/File_Paths/path_distances.txt', 'r').read()
    path_source_target = open('./NBA_Data_Analysis/File_Paths/path_source_target.txt', 'r').read()
    parameters = pd.read_csv(f'./{path_source_target}/experiment_parameters.csv')
    print(parameters)
    file_path = f'./{path_distances}/distance_from_{parameters['instance_1'].values[0]}_to_{parameters['instance_2'].values[0]}.csv'
    df_distances = pd.read_csv(file_path)
    df_distances = df_distances.drop(columns=['Parent_cluster', 'Child_cluster'])

    # List of attributes to calculate standard deviation
    #attributes_list = ['Mean_Signed_Difference', 'Age', 'Gam', 'Win', 'Los', 'Poi', 'FG%', '3P%', 'FT%', 'Tot', 'Ass', 'Tur', 'Ste', 'Blo', 'Per']
    # attributes_list = ['Mean_Signed_Difference', 'Age', 'Gam', 'Win', '3P%', 'Tot', 'Blo']
    attributes_list = df_distances.columns
    # Calculate standard deviations and round to 2 decimal places
    std_values = [np.std(df_distances[attribute]).round(2) for attribute in attributes_list]
    # Create a DataFrame to store standard deviations
    deviations = pd.DataFrame({
        "Attribute": attributes_list,
        "Standard_Deviation": std_values
    })

    # Sort the DataFrame by 'Standard_Deviation'
    deviations = deviations.sort_values(by='Standard_Deviation')
    print(deviations)
    print()
    print(df_distances.columns[2:])
    # Define the dependent and independent variables
    X = df_distances[df_distances.columns[2:]]
    #y = df_distances['Mean_Signed_Difference']
    y = df_distances[df_distances.columns[1]]

    # Correlation matrix
    #corr_matrix = df_distances[['Age', 'Gam', 'Win', 'Los', 'Poi', 'FG%', '3P%', 'FT%','Tot', 'Ass', 'Tur', 'Ste', 'Blo', 'Per']].corr()
    # print(corr_matrix)
    print()

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Set up the XGBoost model
    xg_reg = xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
                            max_depth=5, alpha=10, n_estimators=100)

    # Fit the model to the training data
    xg_reg.fit(X_train, y_train)

    # Make predictions on the test data
    y_pred = xg_reg.predict(X_test)

    # Calculate the mean squared error
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")

    # Get feature importance
    importances = xg_reg.feature_importances_
    feature_importance = pd.DataFrame({'feature': X.columns, 'importance': importances})
    feature_importance = feature_importance.sort_values(by='importance', ascending=False)

    print("Feature Importances:")
    print(feature_importance)


    file_path_regression = open('./NBA_Data_Analysis/File_Paths/path_regression.txt', 'r').read()
    feature_importance.to_csv(f'./{file_path_regression}/feature_importance.csv', index=False)
