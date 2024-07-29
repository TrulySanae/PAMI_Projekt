import random
import pandas as pd
from data_gen_utils import create_customer_profile, pprint, generate_order_df

# Define lists for each parameter
C_max_list = [10, 15, 20]
V_max_list = [30, 50, 70]
sim_weeks_list = [4, 6, 8]
UT_list_list = [[20, 22, 24, 30, 40, 80], [10, 15, 20, 25, 30, 35], [5, 10, 15, 20, 25, 30]]
s = 3

# Number of random profiles to generate
num_profiles = 5

# Function to randomly select a parameter from a list
def select_random_parameter(param_list):
    return random.choice(param_list)

# Function to randomly select K between 1 and 1000
def select_random_K():
    return random.randint(1, 100)
  

# Function to randomly select lambd between 0 and 1
def select_random_lambd():
    return random.uniform(0, 0.2)

## Initialize a DataFrame to store parameters
params = pd.DataFrame(columns=["Dataset", "C_max", "K", "V_max", "lambd", "sim_weeks", "UT_list"])

# Generate customer profiles and their corresponding DataFrames
customer_profiles_list = []
dataframes_list = []

for profile_idx in range(num_profiles):
    C_max = select_random_parameter(C_max_list)
    K = select_random_K()
    V_max = select_random_parameter(V_max_list)
    lambd = select_random_lambd()
    sim_weeks = select_random_parameter(sim_weeks_list)
    UT_list = select_random_parameter(UT_list_list)
    
    # Create a DataFrame for the current row
    current_params = pd.DataFrame([{
        "Dataset": profile_idx ,
        "C_max": C_max,
        "K": K,
        "V_max": V_max,
        "lambd": lambd,
        "sim_weeks": sim_weeks,
        "UT_list": UT_list
    }])
    
    # Append current_params to the params DataFrame
    params = pd.concat([params, current_params], ignore_index=True)
   
    
    customer_profiles = create_customer_profile(C_max, K, V_max, lambd, UT_list)
    customer_profiles_list.append(customer_profiles)
    
    general_df = generate_order_df(customer_profiles, UT_list, sim_weeks)
    dataframes_list.append(general_df)
    
    # Save each DataFrame to a separate CSV file
    csv_filename = f"Output Customer Data/customer_profile_{profile_idx}.csv"
    general_df.to_csv(csv_filename, index=False)

print(params.head(10))
params.to_csv("Output Customer Data/params.csv", index=False)   
# Print the generated customer profiles and corresponding DataFrames
# for i, (profiles, df) in enumerate(zip(customer_profiles_list, dataframes_list)):
#     print(f"Customer Profile Set {i+1}:")
#     pprint.pprint(profiles)
#     print(f"DataFrame for Customer Profile Set {i+1}:")
#     print(df)
#     print("\n")
    
# Save the generated DataFrames to CSV files

