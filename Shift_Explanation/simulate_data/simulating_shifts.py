import random
import pandas as pd
from simulate_data.data_gen_utils import create_customer_profile, pprint, generate_order_df

def datasets_creation(C_max=None, V_max=None, lambd=None, UT_list=None, weight_span=None, num_components=None, number_of_connections=None, K=None, sim_weeks=None, num_profiles=6):
    path_customer_profiles = open('Shift_Explanation/Results_Experiments/File_Paths/path_customer_profiles.txt', 'r').read().strip()
    path_shift_explanations = open('Shift_Explanation/Results_Experiments/File_Paths/path_shift_explanations.txt', 'r').read().strip()

    # Define lists for each parameter
    C_max_list = [10, 15, 20]
    V_max_list = [30, 50, 70]
    sim_weeks_list = [4, 6, 8]
    UT_list_list = [[20, 22, 24, 30, 40, 80], [10, 15, 20, 25, 30, 35], [5, 10, 15, 20, 25, 30]]
    weight_span_list = [[3, 40], [6, 60], [3, 20]]
    num_components_list = [2, 3, 4]
    number_of_connections_list = [1, 2, 3, 4, 5]

    # Function to randomly select a parameter from a list
    def select_random_parameter(param_list):
        return random.choice(param_list)

    # Function to randomly select K between 1 and 100
    def select_random_K():
        return random.randint(1, 100)

    # Function to randomly select lambd between 0.01 and 0.2
    def select_random_lambd():
        return random.uniform(0.01, 0.2)

    params = pd.DataFrame(columns=["Dataset", "C_max", "K", "V_max", "lambd", "sim_weeks", "UT_list", "weight_span", "num_components", "number_of_connections"])

    # Generate customer profiles and their corresponding DataFrames
    customer_profiles_list = []
    dataframes_list = []
    counter = 0

    # Ensure num_profiles has a valid value
    num_profiles = num_profiles if num_profiles is not None else 6

    for i in range(num_profiles // 2):
        # Create profiles with randomized and constant features
        current_sim_weeks = sim_weeks if sim_weeks is not None else select_random_parameter(sim_weeks_list)
        K = K if K is not None else select_random_K()
        for profile_idx in range(2):
            # Assign random values if parameters are not provided
            current_C_max = C_max if C_max is not None else select_random_parameter(C_max_list)
            current_V_max = V_max if V_max is not None else select_random_parameter(V_max_list)
            current_UT_list = UT_list if UT_list is not None else select_random_parameter(UT_list_list)
            current_weight_span = weight_span if weight_span is not None else select_random_parameter(weight_span_list)
            current_num_components = num_components if num_components is not None else select_random_parameter(num_components_list)
            current_number_of_connections = number_of_connections if number_of_connections is not None else select_random_parameter(number_of_connections_list)
            current_lambd = lambd if lambd is not None else select_random_lambd()

            # Create a DataFrame for the current row
            current_params = pd.DataFrame([{
                "Dataset": counter,
                "C_max": current_C_max,
                "K": K,
                "V_max": current_V_max,
                "lambd": current_lambd,
                "sim_weeks": current_sim_weeks,
                "UT_list": current_UT_list,
                "weight_span": current_weight_span,
                "num_components": current_num_components,
                "number_of_connections": current_number_of_connections
            }])
            # Append current_params to the params DataFrame
            params = pd.concat([params, current_params], ignore_index=True)

            # Adjust function call according to actual function definition
            customer_profiles = create_customer_profile(
                current_C_max, K, current_V_max, current_lambd, 
                permissable_unittypes=current_UT_list,  # Adjusted parameter name
                number_of_connections=current_number_of_connections, 
                num_components=current_num_components, 
                weigth_span=current_weight_span  # Corrected spelling
            )
            customer_profiles_list.append(customer_profiles)

            general_df = generate_order_df(customer_profiles, current_UT_list, current_sim_weeks)
            dataframes_list.append(general_df)

            # Save each DataFrame to a separate CSV file
            csv_filename = f"{path_customer_profiles}/customer_profile_{counter}.csv"  # TODO: Change path
            general_df.to_csv(csv_filename, index=False)

            # Increase counter to match Index of customer Data
            counter += 1

    print(params.head(10))
    print("#" * 55)
    print("It worked!")
    params.to_csv(f"{path_shift_explanations}/params.csv", index=False)  # TODO: Change path


    # TODO: Change path
    # Print the generated customer profiles and corresponding DataFrames
    # for i, (profiles, df) in enumerate(zip(customer_profiles_list, dataframes_list)):
    #     print(f"Customer Profile Set {i+1}:")
    #     pprint.pprint(profiles)
    #     print(f"DataFrame for Customer Profile Set {i+1}:")
    #     print(df)
    #     print("\n")

    # Save the generated DataFrames to CSV files

