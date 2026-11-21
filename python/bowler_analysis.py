import pandas as pd

# Load cleaned deliveries data
df = pd.read_csv("dataset/cleaned_deliveries.csv")

# Remove rows where no wicket was taken
wickets = df[
    (df["is_wicket"] == 1) &
    (df["dismissal_kind"] != "run out") &
    (df["dismissal_kind"] != "retired hurt") &
    (df["dismissal_kind"] != "obstructing the field")
]

# Count wickets for each bowler
bowler_wickets = wickets.groupby("bowler")["is_wicket"].count()

# Sort and display top 10 bowlers
top_bowlers = bowler_wickets.sort_values(
    ascending=False
).head(10)

print("\nTOP 10 IPL WICKET-TAKING BOWLERS")
print(top_bowlers)

# Save result
top_bowlers.to_csv("dataset/top_bowlers.csv")

print("\nBowler analysis completed!")

