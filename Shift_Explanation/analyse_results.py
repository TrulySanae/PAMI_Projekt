import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

def create_summary():
  print('analyse_results.py Directory')
  print(os.getcwd())
  # Load the CSV files
  path_distances = open('Shift_Explanation/Results_Experiments/File_Paths/path_distances.txt','r').read()
  for i in range(0,5,2):
      path = f'{path_distances}/results_customer_profile_{i}_and_customer_profile_{i+1}.csv'
      globals()[f'df_{i}'] = pd.read_csv(path)

  # Concatenate the dataframes
  df_combined = pd.concat([df_0, df_2, df_4], ignore_index=True)
  std_con = np.std(df_combined["Connections_diff"]).round(2)
  std_wei = np.std(df_combined["Weight_diff"]).round(2)
  std_uni = np.std(df_combined["Unit_diff"]).round(2)

  deviations = pd.DataFrame({
    "Attribute": ["Connection", "Weight", "UnitType"],
    "Standard_Deviation": [std_con,std_wei,std_uni]
  })
  deviations.sort_values(by='Standard_Deviation')
  path_shift_explanations = open('Shift_Explanation//Results_Experiments/File_Paths/path_shift_explanations.txt','r').read()
  output_path = f"{path_shift_explanations}/Calculated_Variances.csv"
  deviations.to_csv(output_path, index=False)


  # Define the dependent and independent variables
  X = df_combined[['Connections_diff', 'Weight_diff', 'Unit_diff']]
  y = df_combined['Total_distance']
  X = sm.add_constant(X)
  model = sm.OLS(y, X).fit()
  model_summary = model.summary()
  
    # Extract relevant values from the regression summary
  regression_results = {
        "Measurement": ["R-squared", "Adj. R-squared",
                        "const_coef", "const_std_err", "const_p>|t|",
                        "Connections_diff_coef", "Connections_diff_std_err", "Connections_diff_p>|t|",
                        "Weight_diff_coef", "Weight_diff_std_err", "Weight_diff_p>|t|",
                        "Unit_diff_coef", "Unit_diff_std_err", "Unit_diff_p>|t|"],
        "Values": [model.rsquared, model.rsquared_adj,
                    model.params['const'], model.bse['const'], model.pvalues['const'],
                    model.params['Connections_diff'], model.bse['Connections_diff'], model.pvalues['Connections_diff'],
                    model.params['Weight_diff'], model.bse['Weight_diff'], model.pvalues['Weight_diff'],
                    model.params['Unit_diff'], model.bse['Unit_diff'], model.pvalues['Unit_diff']]
    }

    # Convert the dictionary to a dataframe
  regression_results_df = pd.DataFrame(regression_results)

    # Save the dataframe to a CSV file
  regression_results_path = f"{path_shift_explanations}/regression_results.csv"
  regression_results_df.to_csv(regression_results_path, index=False)

  print(model_summary)
  
  # Save the regression results to a text file
  with open(f'{path_shift_explanations}/regression_summary.txt', 'w') as f:
      f.write(model_summary.as_text())
      
