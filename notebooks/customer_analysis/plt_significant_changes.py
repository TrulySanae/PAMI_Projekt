import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Load the dataset
file_path = 'notebooks/customer_analysis/test_daten.csv'
data = pd.read_csv(file_path)

# Aggregate data at the customer level by week
customer_weekly_data = data.groupby(['Customer_id', 'Week']).mean().reset_index()

# Calculate weekly changes for each customer
customer_weekly_data['Weight_shift'] = customer_weekly_data.groupby('Customer_id')['Weight'].diff()
customer_weekly_data['Connection_shift'] = customer_weekly_data.groupby('Customer_id')['Connection'].diff()
customer_weekly_data['Unit_type_shift'] = customer_weekly_data.groupby('Customer_id')['Unit_type'].diff()

# Function to highlight significant changes
def highlight_significant_changes(customer_data, threshold=0.5):
    significant_changes = customer_data[
        (customer_data['Weight_shift'].abs() > threshold) |
        (customer_data['Connection_shift'].abs() > threshold) |
        (customer_data['Unit_type_shift'].abs() > threshold)
    ]
    return significant_changes

# Initialize a list to store significant changes
significant_changes_list = []

# Iterate over each customer and identify significant changes
for customer_id in customer_weekly_data['Customer_id'].unique():
    customer_data = customer_weekly_data[customer_weekly_data['Customer_id'] == customer_id]
    significant_changes = highlight_significant_changes(customer_data)
    significant_changes_list.append(significant_changes)

# Convert the list of significant changes into a DataFrame
significant_changes_df = pd.concat(significant_changes_list, ignore_index=True)

# Output the significant changes
print("Significant changes per customer:")
print(significant_changes_df)

# Optional: Save the significant changes to a CSV file
significant_changes_df.to_csv('significant_changes.csv', index=False)

# Function to create a transport map for a customer
def plot_transport_map(customer_data, customer_id):
    plt.figure(figsize=(12, 6))
    
    plt.plot(customer_data['Week'], customer_data['Weight'], marker='o', label='Weight')
    plt.plot(customer_data['Week'], customer_data['Connection'], marker='o', label='Connection')
    plt.plot(customer_data['Week'], customer_data['Unit_type'], marker='o', label='Unit_type')
    
    plt.xlabel('Week')
    plt.ylabel('Values')
    plt.title(f'Transport Map for Customer {customer_id}')
    plt.legend()
    plt.grid(True)
    plt.show()

# Create transport maps for customers with significant changes
for customer_id in significant_changes_df['Customer_id'].unique():
    customer_data = customer_weekly_data[customer_weekly_data['Customer_id'] == customer_id]
    plot_transport_map(customer_data, customer_id)
