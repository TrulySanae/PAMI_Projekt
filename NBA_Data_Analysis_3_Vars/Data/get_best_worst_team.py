import pandas as pd

# Lesen der Daten aus der Excel-Datei
file_path = 'NBA_Data_Analysis_3_Vars/Data/NBA_Data_Test.xlsx'
data = pd.read_excel(file_path)

df = pd.DataFrame(data)

# Berechne die Anzahl der gespielten Jahre pro Team
team_years = df.groupby('Team')['Year'].nunique()

# Bestimme die Anzahl der Jahre, die alle Teams gleich haben
common_years = team_years.mode().iloc[0]

# Filtere die Teams, die genau diese Anzahl an Jahren gespielt haben
valid_teams = team_years[team_years == common_years].index

# Filtere den ursprünglichen DataFrame nach diesen Teams
filtered_df = df[df['Team'].isin(valid_teams)]

# Berechne die Summe der Net Scores pro Team
team_scores = filtered_df.groupby('Team')['PointsScored'].sum()

# Bestimme das Team mit dem höchsten und dem niedrigsten Net Score
highest_score_team = team_scores.idxmax()
lowest_score_team = team_scores.idxmin()

# Ausgabe der Ergebnisse
print(f"Team mit dem höchsten Net Score: {highest_score_team} (Score: {team_scores[highest_score_team]})")
print(f"Team mit dem niedrigsten Net Score: {lowest_score_team} (Score: {team_scores[lowest_score_team]})")