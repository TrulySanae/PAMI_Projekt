import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

def create_summary():
    # Load the CSV file
    path = 'NBA_Data_Analysis/NBA_results/distance_from_ YEAR <= 2009.csv'
    df_distances = pd.read_csv(path)

    # Define the list of attributes to calculate standard deviation
    attributes_list = [
        'Total_distance', 'Age', 'Gam', 'Win', 'Los', 'Poi', 
        'FG%', '3P%', 'FT%', 'Tot', 'Ass', 'Tur', 'Ste', 'Blo', 'Per'
    ]

    # Calculate standard deviations and create a DataFrame
    deviations = pd.DataFrame({
        "Attribute": attributes_list,
        "Standard_Deviation": [np.std(df_distances[attribute]).round(2) for attribute in attributes_list]
    })

    # Sort the DataFrame by 'Standard_Deviation' in ascending order
    deviations = deviations.sort_values(by='Standard_Deviation')

    # Save the deviations DataFrame to a CSV file
    output_dir = "NBA_Data_Analysis/Results_Experiments"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    deviations.to_csv(os.path.join(output_dir, "Calculated_Variances.csv"), index=False)

    # Define the dependent (y) and independent variables (X)
    X = df_distances[attributes_list[1:]]
    y = df_distances['Total_distance']

    # Add a constant to the independent variables
    X = sm.add_constant(X)

    # Fit the OLS model
    model = sm.OLS(y, X).fit()
    
    # Print the model summary to the console
    print(model.summary())

    # Extract relevant regression results
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

    # Convert the dictionary to a DataFrame and save it
    regression_results_df = pd.DataFrame(regression_results)
    regression_results_df.to_csv(os.path.join(output_dir, "regression_results.csv"), index=False)

    # Save the full regression summary to a text file
    with open(os.path.join(output_dir, "regression_summary.txt"), 'w') as f:
        f.write(model.summary().as_text())

# Run the function
create_summary()
