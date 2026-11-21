
import pandas as pd

# Load cleaned deliveries data
df = pd.read_csv("dataset/cleaned_deliveries.csv")

# Calculate total runs scored by each team
team_runs = df.groupby("batting_team")["total_runs"].sum()

# Sort teams by total runs
top_teams = team_runs.sort_values(
    ascending=False
).head(10)

# Display result
print("\nTOP 10 IPL TEAMS BY TOTAL RUNS")
print(top_teams)

# Save result
top_teams.to_csv("dataset/team_performance.csv")

print("\nTeam analysis completed!")
