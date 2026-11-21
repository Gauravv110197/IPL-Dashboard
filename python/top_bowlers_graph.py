
import pandas as pd
import matplotlib.pyplot as plt

# Read top bowlers data
df = pd.read_csv("dataset/top_bowlers.csv")

# Create bar chart
plt.figure(figsize=(12, 6))

plt.bar(df["bowler"], df["is_wicket"])

plt.title("Top 10 IPL Wicket-Taking Bowlers")
plt.xlabel("Bowlers")
plt.ylabel("Total Wickets")

plt.xticks(rotation=45)
plt.tight_layout()

# Display graph
plt.show()
