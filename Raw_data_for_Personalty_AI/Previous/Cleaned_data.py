import pandas as pd

# Load the dataset
file_path = "sampled_100k_data.csv"  # Update this path if your file is in a different location
data = pd.read_csv(file_path)

# Drop the object columns
columns_to_drop = ['dateload', 'lat_appx_lots_of_err', 'long_appx_lots_of_err']
data_cleaned = data.drop(columns=columns_to_drop, errors='ignore')

# Save the cleaned dataset to a new file
cleaned_file_path = "cleaned_sampled_100k_data.csv"  # Specify the output file name
data_cleaned.to_csv(cleaned_file_path, index=False)

print(f"Cleaned dataset saved to {cleaned_file_path}")
