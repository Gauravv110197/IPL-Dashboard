import pandas as pd
import matplotlib.pyplot as plt

# Read top players data
df = pd.read_csv("dataset/top_players.csv")

# Create bar chart
plt.figure(figsize=(12, 6))

plt.bar(df["batter"], df["Total Runs"])

plt.title("Top 10 IPL Run Scorers")
plt.xlabel("Players")
plt.ylabel("Total Runs")

plt.xticks(rotation=45)
plt.tight_layout()

# Display graph
plt.show()
