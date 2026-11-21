import pandas as pd
import matplotlib.pyplot as plt

# Read team performance data
df = pd.read_csv("dataset/team_performance.csv")

# Create bar chart
plt.figure(figsize=(12, 6))

plt.bar(df["batting_team"], df["total_runs"])

plt.title("IPL Team Performance - Total Runs")
plt.xlabel("IPL Teams")
plt.ylabel("Total Runs")

plt.xticks(rotation=45)
plt.tight_layout()

# Display graph
plt.show()
