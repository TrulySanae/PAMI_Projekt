import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

# Load the dataset
df = pd.read_excel('real_datasets/NBA_Data.xlsx', sheet_name=1)
print(df)

# Function to compare net scores between two teams in the same year
def compare_teams_same_year(team1, team2, year):
    team1_scores = df[(df['TEAM'] == team1) & (df['Year'] == year)]['NetScoreOfPlayer']
    team2_scores = df[(df['TEAM'] == team2) & (df['Year'] == year)]['NetScoreOfPlayer']

    ks_stat, p_value = ks_2samp(team1_scores, team2_scores)
    result = f"KS Statistic: {ks_stat}, p-value: {p_value}\n"

    if p_value < 0.05:
        result += "Distribution shift detected.\n"
        variables = df.columns.drop(['PLAYER', 'TEAM', 'Year'])
        shift_variables = {}

        for var in variables:
            mean_diff = abs(team1_scores.mean() - team2_scores.mean())
            if mean_diff > 0:
                shift_variables[var] = mean_diff

        result += f"Variables responsible for the shift: {shift_variables}\n"
    else:
        result += "No significant distribution shift detected.\n"

    return result


# Function to compare net scores of the same team in different years
def compare_team_diff_years(team, year1, year2):
    year1_scores = df[(df['TEAM'] == team) & (df['Year'] == year1)]['NetScoreOfPlayer']
    year2_scores = df[(df['TEAM'] == team) & (df['Year'] == year2)]['NetScoreOfPlayer']

    ks_stat, p_value = ks_2samp(year1_scores, year2_scores)
    result = f"KS Statistic: {ks_stat}, p-value: {p_value}\n"

    if p_value < 0.05:
        result += "Distribution shift detected.\n"
        variables = df.columns.drop(['PLAYER', 'TEAM', 'Year'])
        shift_variables = {}

        for var in variables:
            mean_diff = abs(year1_scores.mean() - year2_scores.mean())
            if mean_diff > 0:
                shift_variables[var] = mean_diff

        result += f"Variables responsible for the shift: {shift_variables}\n"

        # Check if the shift could be caused by player changes
        players_year1 = set(df[(df['TEAM'] == team) & (df['Year'] == year1)]['PLAYER'])
        players_year2 = set(df[(df['TEAM'] == team) & (df['Year'] == year2)]['PLAYER'])

        joined_players = players_year2 - players_year1
        left_players = players_year1 - players_year2

        result += f"Players who joined between {year1} and {year2}: {joined_players}\n"
        result += f"Players who left between {year1} and {year2}: {left_players}\n"
    else:
        result += "No significant distribution shift detected.\n"

    return result


# Example usage:
# Compare teams DAL and BOS in 2023
print(compare_teams_same_year('DAL', 'BOS', 2023))

# Compare team BOS in 2023 and 2022
print(compare_team_diff_years('BOS', 2023, 2022))
