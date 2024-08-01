import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from scipy.stats import norm
import pprint
import collections
import seaborn as sns
import statistics
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.mixture import GaussianMixture

def pick_randomly_with_normal_distribution(choices, mean, std_deviation, num_samples=1):
    """
    Pick randomly from a list of choices based on a normal distribution.

    Parameters:
        choices (list): List of choices to select from.
        mean (float): Mean of the normal distribution.
        std_deviation (float): Standard deviation of the normal distribution.
        num_samples (int): Number of random samples to pick (default is 1).

    Returns:
        list: List of randomly selected choices.
    """
    if num_samples <= 0:
        raise ValueError("num_samples must be a positive integer.")
    
    # Generate random samples from the normal distribution
    random_samples = np.random.normal(mean, std_deviation, num_samples)
    
    # Clip the random samples to the range of valid indices
    # to ensure they fall within the bounds of the choices list.
    clipped_samples = np.clip(random_samples, 0, len(choices) - 1)
    
    # Round the clipped samples to the nearest integer to get the indices
    # of the choices to be picked.
    indices_to_pick = np.round(clipped_samples).astype(int)
    
    # Select the choices based on the calculated indices.
    randomly_selected_choices = [choices[i] for i in indices_to_pick]
    
    return randomly_selected_choices



def sample_discrete_normal(mean, std_deviation, num_samples=1):
    """
    Sample from a discrete normal distribution.

    Parameters:
        mean (float): Mean of the normal distribution.
        std_deviation (float): Standard deviation of the normal distribution.
        num_samples (int): Number of samples to generate (default is 1).

    Returns:
        numpy.ndarray: Array of randomly sampled discrete values from the normal distribution.
    """
    if num_samples <= 0:
        raise ValueError("num_samples must be a positive integer.")
    
    # Generate random samples from the normal distribution
    continuous_samples = np.random.normal(mean, std_deviation, num_samples)
    
    # Round the continuous samples to the nearest integer to get the discrete values
    discrete_samples = np.round(continuous_samples).astype(int)
    
    return discrete_samples


def plot_gaussian_mixture_model(components):
    """
    Plot the Gaussian Mixture Model based on the components.

    Parameters:
        components (list): List of tuples (mean, std_deviation) for each component.
    """
    x = np.linspace(2, 40, 100)

    plt.figure(figsize=(10, 6))
    
    for i, (mean, std_deviation) in enumerate(components):
        # Calculate the probability density function (PDF) for the normal distribution
        pdf = norm.pdf(x, mean, std_deviation)
        plt.plot(x, pdf, label=f'Component {i+1}')

    plt.xlabel('X')
    plt.ylabel('Density')
    plt.title('Gaussian Mixture Model')
    plt.legend()
    plt.grid(True)
    plt.show()
    
def create_random_mean_covariance(num_components, weight_span):
    """
    Create random mean and covariance matrices for a Gaussian Mixture Model.

    Parameters:
        num_variables (int): Number of variables (size of the mean vector).
        num_components (int): Number of components in the Gaussian Mixture Model.

    Returns:
        list: List containing the random mean and covariance matrices for each component.
    """
    if  num_components <= 0:
        raise ValueError("num_components must be positive integers.")
    
    components = []
    
    for _ in range(num_components):
        # Generate random mean vector with values between 2 and 40
        if weight_span == None:
            mean = np.random.uniform(3, 40, 1)
        mean = np.random.uniform(weight_span[0], weight_span[1], 1)
        
        # Generate a random variances matrix with values between 2 and 10
        var = np.random.uniform(2, 3, 1)

       
        components.append((mean[0],var[0]))
    
    return components


def sample_from_gaussian_mixture_model(components, num_samples=1):
    """
    Sample from the Gaussian Mixture Model.

    Parameters:
        components (list): List of tuples (mean, std_deviation) for each component.
        num_samples (int): Number of samples to generate (default is 1).

    Returns:
        numpy.ndarray: Array of randomly sampled values from the Gaussian Mixture Model.
    """
    num_components = len(components)
    
    if num_samples <= 0:
        raise ValueError("num_samples must be a positive integer.")
    
    # Randomly choose components based on their relative probabilities
    component_indices = np.random.choice(np.arange(num_components), size=num_samples)
    
    samples = []
    
    for idx in component_indices:
        mean, std_deviation = components[idx]
        sample = np.random.normal(mean, std_deviation)
        samples.append(sample)
    
    return np.array(samples)

def order_around_position(arr, position):
    if position < 0 or position >= len(arr):
        raise ValueError("Position is out of range.")

    # Sort the array in descending order
    arr.sort(reverse=True)

    # Get the value at the chosen position
    chosen_value = arr[position]

    # Create a new ordered array
    ordered_array = arr.copy() #[chosen_value]
    ordered_array[position]=arr[0]
    # Index to keep track of the position in the new ordered array
    idx = 1

    # Start from the position and go in both directions
    left, right = position - 1, position + 1
    

    while left >= 0 or right < len(arr):
        if left >= 0:
            ordered_array[left]=arr[idx] #.append(arr[left])
            left -= 1
            idx += 1

        if right < len(arr):
            #print('right',right,arr[idx],len(ordered_array),len(arr),)
            #ordered_array.append(arr[right])
            ordered_array[right]=arr[idx]
            right += 1
            idx += 1
        if idx >= len(arr):
            break

    return ordered_array

def adjust_unittype_id(chosen_unittype,unit_type,permissable_unittypes):
    """
    Adjust the unit type chosen by the sampler to match an existing and permissable unit type.

    Parameters:
        chosen_unittype (int): The sampled unit number
        unit_type (int): The prefered unit type for this order
        permissable_unittypes (list): list of all the allowed unit type numbers

    Returns:
        int: the chosen unit type with adjusted ID number
    """
    if chosen_unittype==unit_type:
        return chosen_unittype
    dev = chosen_unittype-unit_type
    idx_prefered_unit= permissable_unittypes.index(unit_type)
    if idx_prefered_unit+dev < len(permissable_unittypes):
        chosen_unittype = np.array(permissable_unittypes)[idx_prefered_unit+dev]
        return chosen_unittype
    
    chosen_unittype = np.array(permissable_unittypes)[idx_prefered_unit+dev-len(permissable_unittypes)]
    return chosen_unittype

def create_customer_profile(C_max, K, V_max, lambd, permissable_unittypes=[10,18,20,22,24,30,40,80],number_of_connections=None,num_components=3,weigth_span=None):
    C = set(range(1, C_max+1))
   
    available_connections = list(C)
    K_profiles = []
    for k in range(1, K+1):
        V_k = int(np.maximum(np.exp(-lambd * k),0.05) * V_max) #Typical volume for this customer.
        if number_of_connections == None:
            number_of_connections= random.randint(1, C_max)
        customer_profile = {'Customer_id':k,'V_k': V_k,'num_connections':number_of_connections, 'connections': []}
        for c in range(1, number_of_connections + 1):
            connection_kc = np.random.choice(available_connections) #np.random.choice(C)
            order_dist_kc = np.random.randint(1, 4) #Order Distribution during the week.
            freq_order = sample_discrete_normal(1, 0.5, 1)[0] #1 indicates this order is weekley, 2: bi-weekly, 0-sporadic
            if freq_order==2:
                order_prob=np.random.choice([0,1])
            else:
                order_prob=np.random.rand(1)

            if order_dist_kc == 1:#1: There exists a main delivery day
                day_kc = np.random.randint(1, 6)
            elif order_dist_kc == 2:## 2: there exit two main delivery day
                day_kc = np.random.choice(range(1,6), 2, replace=False)
            else:# 3: orders are consistent across the weekdays
                day_kc = None

            V_kc = int((c / sum(range(1, number_of_connections + 1))) * V_k) #Divide the total customer volumes across the destinations.
            unit_type = np.random.choice(permissable_unittypes) #Main unit used by customer k in this connection
            unittype_std = np.random.random() # standard deviation of not picking the prefered unit

            #We  assume that the weights of units in a particular connection are sampled from Gaussian mixture model .
            components =create_random_mean_covariance(num_components, weigth_span)


            arrival_hour= np.random.randint(1, 22)
            delivery_deadline= np.random.randint(3,10)

            customer_profile['connections'].append({
                'connection_kc': connection_kc, 
                'order_dist_kc': order_dist_kc, # Order Distribution during the week.
                'freq_order':freq_order,
                'order_prob':order_prob,
                'day_kc': day_kc,# Prefered delivery day 
                'V_kc': V_kc, # Volume of that connection
                'unit_type': unit_type, # Prefered Unit type
                'unittype_std': unittype_std,# Deviation from that unit
                'weights_components': components, # Distribution of the unit weights
                'arrival_hour':arrival_hour,
                'delivery_deadline':delivery_deadline
            })

        K_profiles.append(customer_profile)

    return K_profiles





import math
def sample_orders(customer_profiles, tau_week,even_week=0,permissable_unittypes=[10,18,20,22,24,30,40,80],sample_time=False):
    current_orders = []
    for k, profile in enumerate(customer_profiles):
        V_k = profile['V_k']
        C_k = profile['num_connections']
        Customer_id = profile['Customer_id']
        # Check if the customer should be included in this week's plan
        for connection in profile['connections']:
            if connection['freq_order']==0:#sporadic orders
                if np.random.rand(1)<connection['order_prob']:
                    continue
            elif connection['freq_order']==2:# biweekly
                if connection['order_prob']!=even_week:
                    continue
                    
            connection_kc = connection['connection_kc'] #Current Connection 
            order_dist_kc = connection['order_dist_kc'] #Order distribution across the week
            day_kc = connection['day_kc'] #Main day of order arrival
            V_kc = connection['V_kc'] #Volume across the week
            unit_type = connection['unit_type']#most common unit type
            unittype_std = connection['unittype_std']#variance of the unit type
            
            weights_components = connection['weights_components'] #distribution of the order weights
            
            if order_dist_kc == 1:  # Most orders arrive on a specific day of the week
                order_volumes = np.random.rand(5).tolist() #np.random.normal(1+tau_week, 0.2 , 5)
                order_volumes = np.array(order_around_position(order_volumes, day_kc-1))
                order_volumes= np.concatenate((order_volumes,np.random.normal(0.2,0.05,2)))
            elif order_dist_kc == 2:  # Most orders arrive on two specific days of the week
                order_volumes = np.random.rand(5).tolist() 
                order_volumes = (np.array(order_around_position(order_volumes, day_kc[0]-1))+np.array(order_around_position(order_volumes, day_kc[1]-1)))/2
                order_volumes= np.concatenate((order_volumes,np.random.normal(0.2,0.05,2)))
            else:
                order_volumes = np.ones(5)-np.random.normal(0.2,0.1,5)
                order_volumes= np.concatenate((order_volumes,np.random.normal(0.2,0.05,2)))
            order_volumes = np.clip(order_volumes * (V_kc+int(V_kc *tau_week)), 0, (V_kc+int(V_kc *tau_week)))  #Ensure non-negative volumes
            #print(connection_kc,V_kc,order_volumes)
            for day, daily_orders in enumerate(order_volumes, start=1):
                #print('daily orders',daily_orders,math.ceil(daily_orders))
                for _ in range(math.ceil(daily_orders)):
                    weight = sample_from_gaussian_mixture_model(weights_components) #np.random.multivariate_normal(mu_kc,cov_kc, 1)
                    weight =np.clip(weight, 3, None)
                    chosen_unittype =sample_discrete_normal(unit_type,unittype_std,1)
                    #TODO Adjust the chosen SD based on the availabe types of units
                    chosen_unittype = adjust_unittype_id(chosen_unittype,unit_type,permissable_unittypes)
                    if sample_time:
                        arrival_time = connection['arrival_hour'] + np.random.randint(0, 2)
                        delivery_deadline = connection['delivery_deadline'] + np.random.randint(0, 2)
                        current_orders.append((Customer_id, connection_kc, weight[0],chosen_unittype[0], day,arrival_time,delivery_deadline))
                    else:
                        current_orders.append((Customer_id, connection_kc, weight[0],chosen_unittype[0], day))

    return current_orders



def generate_order_df(customer_profiles,UT_list, sim_weeks=10,sample_time=False):
    general_df = pd.DataFrame()
    for week in range(sim_weeks): # 
        tau_week = 0.01 #np.random.normal(0.05, 0.15, 1)[0]
        current_orders = sample_orders(customer_profiles, tau_week,even_week= week % 2,permissable_unittypes= UT_list,sample_time=sample_time)
        #print(current_orders)
        if sample_time:
            df_orders= pd.DataFrame(current_orders, columns=['Customer_id', 'Connection', 'Weight','Unit_type','Day','Arrival Time','Delivery Deadline'])
        else:
            df_orders= pd.DataFrame(current_orders, columns=['Customer_id', 'Connection', 'Weight','Unit_type','Day'])

        #df_orders['Day'] += (7*week)
        df_orders['Week'] = [week] * len(df_orders)
        general_df = pd.concat([general_df, df_orders], ignore_index=True)
    return general_df


def generate_multi_order_df(customer_profiles,UT_list,orders_per_row, sim_weeks=10):
    general_df = pd.DataFrame()
    for week in range(sim_weeks): # 
        tau_week =np.random.normal(0.05, 0.15, 1)[0]
        current_orders = sample_orders(customer_profiles, tau_week,even_week= week % 2,permissable_unittypes= UT_list)
        #print(current_orders)
        df_orders= pd.DataFrame(current_orders, columns=['Customer_id', 'Connection', 'Weight','Unit_type','Day'])
        for column_name in ['Customer_id','Connection','Weight','Unit_type','Day']:  
            df_orders[column_name] = df_orders[column_name].astype(str)
        #df_orders['Day'] += (7*week)
        for i in range(len(df_orders)):
            condition = df_orders['Customer_id'] == df_orders['Customer_id'][i]
            filtered_df = df_orders[condition]
            # Choose the number of random rows to concatenate
            num_random_rows = orders_per_row
            #TODO You should only allow replacement for those with less than 3 rows 
            random_indices = np.random.choice(filtered_df.index, size=num_random_rows, replace=True)
    
            # Extract the random rows using the random indices
            random_rows = filtered_df.loc[random_indices]
            #random_rows = pd.concat([random_rows,df_orders.iloc[i]], ignore_index=True)
            # Enumerate column names and values for the random rows
            #concatenated_row = pd.concat([random_rows], axis=0, ignore_index=True)
            concatenated_row  = random_rows.groupby('Customer_id').agg({
            'Connection': ', '.join,
            'Weight': ', '.join,
            'Unit_type': ', '.join,
            'Day': ', '.join
            }).reset_index()#random_rows.groupby('Customer_id').apply(' '.join).reset_index()
            for column_name in ['Connection','Weight','Unit_type','Day']:  
                new_columns = concatenated_row[column_name].str.split(',', expand=True)
                new_columns.columns = [f'{column_name}_{i+1}' for i in range(new_columns.shape[1])]
                concatenated_row = pd.concat([concatenated_row, new_columns], axis=1)
            concatenated_row['Week'] = week #[week] * len(df_orders)
            # Split the 'values' column by comma and expand into new columns
            general_df = pd.concat([general_df, concatenated_row], ignore_index=True)
    
    return general_df

def estimate_customer_profiles(orders_history, cutoff=500,subset_size=30):
    #get number of customers with a count above a certain threshold
    #filter the df for each  customer
    #For each connection, 
    #For each Unit Type
    #Estimate Freq Order Weekly, Bi-weekly or sporadic 
    #estimate the weekly volume for this pair
    #estimate the weekly pattern check if it a uniform or a gaussian distro
    #mixture of gaussian for the weights
    #get a Gaussian for the unit types
   
    grouped= orders_history.groupby('Customer_id').count().reset_index()
    print('total customers',len(grouped))
    grouped= grouped[grouped['Connection'] > cutoff]
    print('total customers after cutoff',len(grouped))
    reference_list = grouped['Customer_id'].tolist()
    print('Customers IDs:',reference_list)
    general_df= orders_history[orders_history['Customer_id'].isin(reference_list)]
    K_profiles = []
    num_simulation_weeks= len(orders_history['Week'].unique())
    for customer in reference_list:
        customer_orders = general_df[general_df['Customer_id'] == customer]
        # Get the unique values from the 'Column_name' column
        unique_connections = customer_orders['Connection'].unique()
        # Convert the unique values to a list
        unique_connections_list = list(unique_connections)
        #customer_profile = {'V_k': V_k,'num_connections':number_of_connections, 'connections': []}
        #print(unique_connections_list, f'unique connections for customer {customer}')
        number_of_connections=0
        V_k=0
        customer_profile = {'Customer_id':customer, 'V_k': V_k,'num_connections': number_of_connections, 'connections': []}
        for current_connection in unique_connections_list:
            connection_customer_pairs= customer_orders[customer_orders['Connection'] == current_connection]
            unique_unit_types = list(customer_orders['Unit_type'].unique())
            #print(f'Customer{customer}, Connection {current_connection},Unique Units {unique_unit_types}')
            for unit_type in unique_unit_types:

                #Estimate the user profile using this
                connection_customer_unitType= connection_customer_pairs[connection_customer_pairs['Unit_type'] == unit_type]
                data =connection_customer_unitType["Weight"].to_numpy()
                if len(data)<subset_size:
                    continue
                number_of_connections +=1

                # Define the number of components in the mixture
                n_components = 3
                
                # Initialize the Gaussian Mixture Model
                gmm = GaussianMixture(n_components=n_components, random_state=0)
                
                # Fit the GMM to the data to estimate the parameters
                gmm.fit(data.reshape(-1, 1))
                means = gmm.means_
                
                #Estimated standard deviations of the Gaussian components
                std_devs = np.sqrt(gmm.covariances_)
                
                #Mixing coefficients (weights) of the Gaussian components
                #weights = gmm.weights_

                components = [(x, y) for x, y in zip(gmm.means_[:,0], std_devs[:,0,0])]

                grouped_counts_per_week = connection_customer_unitType.groupby('Week').count().to_numpy()
                grouped_counts_per_day = connection_customer_unitType.groupby('Day').count().to_numpy()

                day_wise_counts=grouped_counts_per_day[:5,0]
                sorted_indices = np.argsort(day_wise_counts)[::-1]
                # Get the two largest values using the sorted indices
                largest_values = day_wise_counts[sorted_indices[:2]]

                V_kc= np.max(grouped_counts_per_day[:,0]/num_simulation_weeks)
                V_kc = math.ceil(V_kc)  
                #print(np.min(day_wise_counts[:5]),np.max(day_wise_counts[:5]),largest_values[1],largest_values[0])
                if np.min(day_wise_counts[:5])/np.max(day_wise_counts[:5]) >0.7 :
                    #print('mode 1',grouped_counts[:,0])
                    order_dist_kc=3
                    #V_kc= np.mean(grouped_counts[:,0])/5
                    day_kc=None
                elif largest_values[1]/largest_values[0] >0.8:
                    #print('mode 2',grouped_counts[:,0])
                    order_dist_kc=2
                    #V_kc=np.mean(grouped_counts[:,0])#/num_simulation_weeks
                    day_kc= sorted_indices[:2]+1
                else:
                    #print('mode 3',grouped_counts[:,0])
                    order_dist_kc= 1
                    #V_kc=np.mean(grouped_counts[:,0])#/num_simulation_weeks
                    day_kc= sorted_indices[0]+1
                V_k=V_k+V_kc
                unique_weeks= np.unique(connection_customer_unitType['Week'].to_numpy())
                order_prob= unique_weeks.shape[0]/num_simulation_weeks
                
                if order_prob==1.0:
                    freq_order = 1
                elif order_prob==0.5:
                    # Check if elements are even or odd
                    even_mask = unique_weeks % 2 == 0  # Creates a boolean mask for even numbers
                    odd_mask = unique_weeks % 2 != 0   # Creates a boolean mask for odd numbers
                    if even_mask.size == 0:
                        order_prob=1 #we have orders on the uneven week
                        freq_order =2
                    elif odd_mask.size == 0:
                        order_prob=0 #we have orders on the uneven week
                        freq_order=2
                    else:
                        freq_order=0
                else:
                    freq_order=0

                
                customer_profile['connections'].append({
                'connection_kc': current_connection, 
                'order_dist_kc': order_dist_kc, #Order Distribution during the week.
                'freq_order': freq_order,
                'order_prob': order_prob,
                'day_kc': day_kc,#prefered delivery day 
                'V_kc': V_kc, #Volume of that connection
                'unit_type': unit_type, # Prefered Unit type
                'unittype_std': 0.05,# Deviation from that unit
                'weights_components': components, #Distribution of the unit weights
                })
        customer_profile['V_k'] = V_k
        customer_profile['num_connections'] = number_of_connections
        K_profiles.append(customer_profile)
    return K_profiles

def check_corresponding_row(target_row,df,weight=True,weight_tolerance=3):
    result = df[df['Customer_id']==target_row[0]]
    result = result[result['Connection']==target_row[1]]
    result = result[result['Day']==target_row[4]]
    #result = result[result['Week']==target_row[5]]
    result = result[result['Unit_type']==target_row[3]]
    if weight:
        result = result[result['Weight']>=target_row[2]- weight_tolerance]
        result = result[result['Weight']<=target_row[2]+ weight_tolerance]    
    return result
#check_corresponding_row(filtered_rows.iloc[5].to_numpy(),df_real,weight_tolerance=5)
import pandas as pd

def estimate_accuracy(df_real,df_predicted,weight=True):
    # Iterate through each row in the DataFrame
    acc=0
    for index, row in df_real.iterrows():
        # Access the values in each column for the current row
        obtained_df= check_corresponding_row(row,df_predicted,weight,weight_tolerance=5)
        # Check the condition for the current row
        if not obtained_df.empty:
            acc+=1
    return acc/index
        
def data_split(data):
    week_0 = data[data['Week'] == 0]
    other_weeks = data[data['Week'] != 0]
    return week_0, other_weeks


            
        



