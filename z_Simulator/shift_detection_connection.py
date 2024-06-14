import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ks_2samp

# TODO: Eventuell kann man diesen Code als Inspiration nutzen, um nach bestimmten Variablen zu gruppieren.
# Assuming you have the data in a DataFrame df with relevant columns
# For example, df = pd.read_csv('your_data_file.csv')

# Generate some example data
np.random.seed(0)
df = pd.DataFrame({
    'Customer_id': np.arange(1, 201),
    'Connection': np.random.poisson(lam=5, size=200),
    'Weight': np.random.rand(200),
    'Unit_type': np.random.choice([20, 22, 24, 30, 40, 80], 200),
    'Day': np.random.randint(1, 31, 200),
    'Week': np.random.randint(1, 6, 200)
})


# Function to detect significant shifts and visualize
def detect_distribution_shifts(df, column, group_by, alpha=0.05):
    unique_groups = df[group_by].unique()
    results = []

    for i in range(len(unique_groups) - 1):
        for j in range(i + 1, len(unique_groups)):
            group1 = df[df[group_by] == unique_groups[i]][column]
            group2 = df[df[group_by] == unique_groups[j]][column]

            # Perform the Kolmogorov-Smirnov test
            ks_stat, p_value = ks_2samp(group1, group2)

            if p_value < alpha:
                results.append((unique_groups[i], unique_groups[j], ks_stat, p_value))

    return results


# Detect shifts in Connection levels between different Weeks
group_by = 'Weight'
shifts = detect_distribution_shifts(df, 'Connection', group_by)


# Visualize the distributions and shifts
def visualize_shifts(df, column, group_by, shifts):
    plt.figure(figsize=(14, 8))
    sns.boxplot(x=group_by, y=column, data=df)
    plt.title(f'Distribution of {column} across different {group_by}s')
    plt.show()

    if shifts:
        for shift in shifts:
            group1, group2, ks_stat, p_value = shift
            plt.figure(figsize=(12, 6))
            sns.kdeplot(df[df[group_by] == group1][column], label=f'{group_by} {group1}', shade=True)
            sns.kdeplot(df[df[group_by] == group2][column], label=f'{group_by} {group2}', shade=True)
            plt.title(
                f'Significant Distribution Shift Detected: {group_by} {group1} vs {group_by} {group2}\nKS Statistic={ks_stat:.4f}, p-value={p_value:.4f}')
            plt.legend()
            plt.show()


# Visualize the detected shifts
visualize_shifts(df, 'Connection', group_by, shifts)


# Provide standardized explanations for the shifts
def explain_shifts(shifts, group_by):
    explanations = []
    for shift in shifts:
        group1, group2, ks_stat, p_value = shift
        explanation = (
            f"Significant distribution shift detected between {group_by} {group1} and {group_by} {group2}. "
            f"The KS Statistic is {ks_stat:.4f} with a p-value of {p_value:.4f}. "
            "Possible explanations for this shift could include changes in customer behavior, "
            "marketing strategies, external events impacting customer engagement, or data collection inconsistencies."
        )
        explanations.append(explanation)
    return explanations


# Print standardized explanations
explanations = explain_shifts(shifts, group_by)
for explanation in explanations:
    print(explanation)
