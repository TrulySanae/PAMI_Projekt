import random
import pandas as pd
from data_gen_utils import create_customer_profile, pprint, generate_order_df


# Define lists for each parameter
C_max_list = [10, 15, 20]
V_max_list = [30, 50, 70]
sim_weeks_list = [4, 6, 8]
UT_list_list = [[20, 22, 24, 30, 40, 80], [10, 15, 20, 25, 30, 35], [5, 10, 15, 20, 25, 30]]
weight_span_list = [[3,40],[6, 60], [3,20]]
num_components_list = [2, 3, 4]
number_of_connections_list = [1, 2, 3, 4, 5]

# Number of random profiles to generate
num_profiles = int(6)

# Function to randomly select a parameter from a list
def select_random_parameter(param_list):
    return random.choice(param_list)

# Function to randomly select K between 1 and 100
def select_random_K():
    return random.randint(1, 100)
  

# Function to randomly select lambd between 0 and 1
def select_random_lambd():
    return random.uniform(0.01, 0.2)

params = pd.DataFrame(columns=["Dataset", "C_max", "K", "V_max", "lambd", "sim_weeks", "UT_list"])

# Generate customer profiles and their corresponding DataFrames
customer_profiles_list = []
dataframes_list = []

counter = 0
for i in range(num_profiles//2):
    # Constant features for one set of generated profiles
    # sim_weeks = select_random_parameter(sim_weeks_list)
    # K = select_random_K()
    K = 50
    sim_weeks = 6
    C_max = 20
    V_max = 50
    lambd = 0.1
    UT_list = [20, 20, 20, 20, 20, 20]
    weight_span = [3,40]
    num_components = 3
    number_of_connections = 5


    # Create profiles with randomized and constant features
    for profile_idx in range(2):
        #C_max = select_random_parameter(C_max_list)
        #V_max = select_random_parameter(V_max_list)
        #lambd = select_random_lambd()
        #UT_list = select_random_parameter(UT_list_list)
        # weight_span = select_random_parameter(weight_span_list)
        #num_components = select_random_parameter(num_components_list)
        #number_of_connections = select_random_parameter(number_of_connections_list)
        

        # Create a DataFrame for the current row
        current_params = pd.DataFrame([{
            "Dataset": counter,
            "C_max": C_max,
            "K": K,
            "V_max": V_max,
            "lambd": lambd,
            "sim_weeks": sim_weeks,
            "UT_list": UT_list,
            "weight_span": weight_span,
            "num_components": num_components,
            "number_of_connections": number_of_connections
        }])
        # Append current_params to the params DataFrame
        params = pd.concat([params, current_params], ignore_index=True)


        customer_profiles = create_customer_profile(C_max, K, V_max, lambd, UT_list,weigth_span=weight_span, num_components=num_components, number_of_connections=number_of_connections)
        customer_profiles_list.append(customer_profiles)

        general_df = generate_order_df(customer_profiles, UT_list, sim_weeks)
        dataframes_list.append(general_df)

        # Save each DataFrame to a separate CSV file
        csv_filename = f"/Users/sanaemessoudi/Desktop/Projekte/PAMI_Projekt9/Shift Explantion/00_simulate_data/Output Customer Data/customer_profile_{counter}.csv" # TODO: Change path
        general_df.to_csv(csv_filename, index=False)

        # Increase counter to match Index of customer Data
        counter += 1

print(params.head(10))
params.to_csv("/Users/sanaemessoudi/Desktop/Projekte/PAMI_Projekt9/Shift Explantion/00_simulate_data/Output Customer Data/params.csv", index=False) # TODO: Change path
# Print the generated customer profiles and corresponding DataFrames
# for i, (profiles, df) in enumerate(zip(customer_profiles_list, dataframes_list)):
#     print(f"Customer Profile Set {i+1}:")
#     pprint.pprint(profiles)
#     print(f"DataFrame for Customer Profile Set {i+1}:")
#     print(df)
#     print("\n")
    
# Save the generated DataFrames to CSV files

