import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

def create_summary():
    # Load the CSV file
    path_distances = open('./NBA_Data_Analysis_3_Vars/File_Paths/path_distances.txt', 'r').read()
    path_source_target = open('./NBA_Data_Analysis_3_Vars/File_Paths/path_source_target.txt', 'r').read()
    parameters = pd.read_csv(f'./{path_source_target}/experiment_parameters.csv')
    print(parameters)
    file_path = f'./{path_distances}/distance_from_{parameters['instance_1'].values[0]}_to_{parameters['instance_2'].values[0]}.csv'
    df_distances = pd.read_csv(file_path)
    df_distances = df_distances.drop(columns=['Parent_cluster', 'Child_cluster'])

    # List of attributes to calculate standard deviation
    attributes_list = list(df_distances.columns)

    # Calculate standard deviations and round to 2 decimal places
    std_values = [np.std(df_distances[attribute]).round(2) for attribute in attributes_list]
    # Create a DataFrame to store standard deviations
    deviations = pd.DataFrame({
        "Attribute": attributes_list,
        "Standard_Deviation": std_values
    })

    # Sort the DataFrame by 'Standard_Deviation'
    deviations = deviations.sort_values(by='Standard_Deviation')
    # Save the deviations DataFrame to a CSV file
    # output_path = "NBA_Data_Analysis/Results_Experiments/Calculated_Variances.csv"
    # deviations.to_csv(output_path, index=False)
    # Define the dependent and independent variables
    X = df_distances[attributes_list[2:]]
    y = df_distances[attributes_list[1]]

    # Add a constant to the independent variables
    X = sm.add_constant(X)
    # Fit the OLS model
    model = sm.OLS(y, X).fit()
    model_summary = model.summary()
    # Extract relevant values from the regression summary
    regression_results = {
        "Measurement": ["R-squared", "Adj. R-squared", "const_coef", 
                        "const_std_err", "const_p>|t|"],
        "Values": [model.rsquared, model.rsquared_adj,
                   model.params['const'], model.bse['const'], model.pvalues['const']]
    }
    # Extract coefficients, standard errors, and p-values for all variables
    for var in X.columns[1:]:  # Skip 'const'
        regression_results["Measurement"].extend([f"{var}_coef", f"{var}_std_err", f"{var}_p>|t|"])
        regression_results["Values"].extend([model.params[var], model.bse[var], model.pvalues[var]])
    print(model_summary)



    file_path_regression = open('./NBA_Data_Analysis_3_Vars/File_Paths/path_regression.txt', 'r').read()

    # Save the regression summary to a text file
    with open(file_path_regression+'/regression_results.txt', 'w') as f:
        f.write(model_summary.as_text())

# create_summary()
