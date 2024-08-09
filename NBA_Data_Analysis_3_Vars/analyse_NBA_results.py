import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

def create_summary():
    # Load the CSV file
    path = 'NBA_Data_Analysis/NBA_results/distance_from_BOS.csv'
    df_distances = pd.read_csv(path)

    # List of attributes to calculate standard deviation
    attributes_list = ['Total_distance', 'Age', 'Gam', 'Win', 'Los', 
                       'Poi', 'FG%', '3P%', 'FT%', 'Tot', 'Ass', 'Tur', 'Ste', 'Blo', 'Per']

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
    output_path = "NBA_Data_Analysis/Results_Experiments/Calculated_Variances.csv"
    deviations.to_csv(output_path, index=False)
    # Define the dependent and independent variables
    X = df_distances[['Age', 'Gam', 'Win', '3P%', 'Tot', 'Blo']]
    y = df_distances['Total_distance']

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
    # Convert the dictionary to a DataFrame
    regression_results_df = pd.DataFrame(regression_results)
    # Save the regression results to a CSV file
    regression_results_path = "NBA_Data_Analysis/Results_Experiments/regression_results.csv"
    regression_results_df.to_csv(regression_results_path, index=False)
    # Print the model summary to the console
    print(model_summary)





    # Save the regression summary to a text file
    summary_output_path = "NBA_Data_Analysis/Results_Experiments/regression_summary.txt"
    with open(summary_output_path, 'w') as f:
        f.write(model_summary.as_text())

create_summary()
