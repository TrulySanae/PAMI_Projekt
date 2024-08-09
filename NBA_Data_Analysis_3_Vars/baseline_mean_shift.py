import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


parameters = pd.read_csv('NBA_Data_Analysis_3_Vars/Source_Target/experiment_parameters_GSW_vs_POR.csv')
team1 = parameters['instance_1'].values[0]
team2 = parameters['instance_2'].values[0]
# Laden Sie die Daten
team1_data = pd.read_csv('NBA_Data_Analysis_3_Vars/Source_Target/source_data_GSW.csv')
team2_data = pd.read_csv('NBA_Data_Analysis_3_Vars/Source_Target/target_data_POR.csv')

# Fügen Sie eine Spalte hinzu, um das Team zu kennzeichnen
team1_data['Team'] = team1
team2_data['Team'] = team2

# Kombinieren Sie die Daten
data = pd.concat([team1_data, team2_data])

# Normieren Sie die Daten
data['NetScore_norm'] = (data['NetScoreOfPlayer'] - data['NetScoreOfPlayer'].mean()) / data['NetScoreOfPlayer'].std()
data['Age_norm'] = (data['Age'] - data['Age'].mean()) / data['Age'].std()
data['GamesPlayed_norm'] = (data['GamesPlayed'] - data['GamesPlayed'].mean()) / data['GamesPlayed'].std()

# Bereiten Sie die Daten für das Plotten vor
melted_data = pd.melt(data, id_vars='Team', value_vars=['NetScore_norm', 'Age_norm', 'GamesPlayed_norm'])

# Plot
plt.figure(figsize=(10, 6))
sns.stripplot(x='value', y='variable', hue='Team', data=melted_data, dodge=True, orient='h', 
              palette='coolwarm', alpha=0.7)

# Anpassen der Achsen und des Layouts
plt.axvline(0, color='gray', linestyle='--')
plt.xlabel('Standardized Values')
plt.ylabel('')
plt.title(f'Comparison between {team1} and {team2}')
plt.legend(title='Team', loc='upper right')
plt.show()