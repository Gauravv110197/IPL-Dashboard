import pandas as pd
# Load cleaned deliveries data
df = pd.read_csv("dataset/cleaned_deliveries.csv")

# Calculate total runs scored by each player
player_runs = df.groupby("batter")["batsman_runs"].sum()

# Calculate balls faced
balls_faced = df[df["extras_type"] != "wides"].groupby("batter")["ball"].count()

# Combine runs and balls
analysis = pd.DataFrame({
    "Total Runs": player_runs,
    "Balls Faced": balls_faced
}).fillna(0)

# Calculate strike rate
analysis["Strike Rate"] = (
    analysis["Total Runs"] / analysis["Balls Faced"] * 100
).round(2)

# Display top 10 players
top_players = analysis.sort_values(
    by="Total Runs", ascending=False
).head(10)

print("\nTOP 10 IPL RUN SCORERS")
print(top_players)

# Save analysis
top_players.to_csv("dataset/top_players.csv")

print("\nPlayer analysis completed!")
