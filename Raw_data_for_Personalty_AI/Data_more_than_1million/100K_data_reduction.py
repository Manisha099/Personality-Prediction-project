import pandas as pd

# Load the cleaned dataset
data = pd.read_csv('/Users/robin/Desktop/cleaned_data-final.csv')

# Randomly sample 100,000 rows
sampled_data = data.sample(n=100000, random_state=42)

# Save the sampled data to a new CSV file
sampled_data.to_csv('sampled_100k_data.csv', index=False)

print("Sampled 100,000 rows and saved to 'sampled_100k_data.csv'")
