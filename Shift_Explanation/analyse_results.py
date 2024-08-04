import pandas as pd
import numpy as np
import statsmodels.api as sm

def create_summary():
  # Load the CSV files
  path_distances = open('./Results_Experiments/File_Paths/path_distances.txt','r').read()
  for i in range(0,5,2):
      path = f'../{path_distances}/results_customer_profile_{i}_and_customer_profile_{i+1}.csv'
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
  path_shift_explanations = open('./Results_Experiments/File_Paths/path_shift_explanations.txt','r').read()
  output_path = f"../{path_shift_explanations}/Calculated_Variances.csv"
  deviations.to_csv(output_path, index=False)


  # Define the dependent and independent variables
  X = df_combined[['Connections_diff', 'Weight_diff', 'Unit_diff']]
  y = df_combined['Total_distance']
  X = sm.add_constant(X)
  model = sm.OLS(y, X).fit()
  model_summary = model.summary()
  # Save the regression results to a text file
  with open(f'../{path_shift_explanations}/regression_summary.txt', 'w') as f:
      f.write(model_summary.as_text())
      
  print(model_summary)