from data_gen_utils import create_customer_profile, pprint, generate_order_df

# Example usage:
C_max = 10 # Number of connections
K = 100 #Number of Customers
V_max = 30 #Max Volume for one day for a customer
lambd = 0.05 #Exponential decay of total volume between customers. Higher values indicate that less customers are responsible for most orders
sim_weeks = 5 #Number of Simulation Weeks
UT_list = [20, 22, 24, 30, 40, 80] #different unit types

customer_profiles = create_customer_profile(C_max, K, V_max, lambd,UT_list)

print('++++++++++++++Visualization of Customer Profies++++++++++++++++')
for customer in customer_profiles:
    pprint.pprint(customer, indent=4)
general_df = generate_order_df(customer_profiles, UT_list, sim_weeks=5)