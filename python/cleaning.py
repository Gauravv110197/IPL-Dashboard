
import pandas as pd

# Load IPL datasets
matches = pd.read_csv("dataset/matches.csv")
deliveries = pd.read_csv("dataset/deliveries.csv")

# Display original dataset size
print("Original Matches:", matches.shape)
print("Original Deliveries:", deliveries.shape)

# Remove duplicate rows
matches = matches.drop_duplicates()
deliveries = deliveries.drop_duplicates()

# Handle missing values
matches = matches.dropna(subset=["id"])
deliveries = deliveries.fillna({
    "extras_type": "None",
    "player_dismissed": "None",
    "dismissal_kind": "None",
    "fielder": "None"
})

# Save cleaned datasets
matches.to_csv("dataset/cleaned_matches.csv", index=False)
deliveries.to_csv("dataset/cleaned_deliveries.csv", index=False)

print("Data cleaning completed!")
print("Cleaned Matches:", matches.shape)
print("Cleaned Deliveries:", deliveries.shape)
