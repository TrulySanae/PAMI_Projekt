from data_gen_utils import create_customer_profile, pprint, generate_order_df

"""In this module we will create artifical datashifts in our simulateted data"""

C_max = 10 # Number of connections
K = 100 #Number of Customers
V_max = 30 #Max Volume for one day for a customer
lambd = 0.05 #Exponential decay of total volume between customers. Higher values indicate that less customers are responsible for most orders
sim_weeks = 6 #Number of Simulation Weeks
UT_list = [20, 22, 24, 30, 40, 80] #different unit types

# Simulate data for 6 weeks and then double the weights for the last 3 weeks

customer_profiles_1 = create_customer_profile(C_max, K, V_max, lambd,UT_list)

data_1= generate_order_df(customer_profiles_1, UT_list, sim_weeks)

# double the weights for the last 3 weeks

data_1.loc[data_1['Week'] >= 3, 'Weight'] *= 2

data_1.to_csv('data_weightshift.csv', index=False)