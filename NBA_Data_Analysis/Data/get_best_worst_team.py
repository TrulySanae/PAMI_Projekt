import pandas as pd

# Erstellen Sie einen DataFrame mit den relevanten Daten
file_path = 'NBA_Data_Analysis/Data/NBA_Data_Test.xlsx'
data = pd.read_excel(file_path)


df = pd.DataFrame(data)

# Berechne die Summe der Net Scores pro Team
team_scores = df.groupby('Team')['PointsScored'].sum()

# Bestimme das Team mit dem höchsten und dem niedrigsten Net Score
highest_score_team = team_scores.idxmax()
lowest_score_team = team_scores.idxmin()

# Ausgabe der Ergebnisse
print(f"Team mit dem höchsten Net Score: {highest_score_team} (Score: {team_scores[highest_score_team]})")
print(f"Team mit dem niedrigsten Net Score: {lowest_score_team} (Score: {team_scores[lowest_score_team]})")