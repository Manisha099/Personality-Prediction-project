import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the dataset
data = pd.read_csv('/Users/robin/Desktop/data-final.csv', sep='\t')

# Step 1: Remove Missing Values
print("Initial data shape:", data.shape)
data.dropna(inplace=True)
print("Data shape after dropping missing values:", data.shape)

# Step 2: Remove Duplicates
data.drop_duplicates(inplace=True)
print("Data shape after removing duplicates:", data.shape)

# Step 3: Drop Unnecessary Columns
# Assuming the 'country' column is unnecessary
if 'country' in data.columns:
    data = data.drop(['country'], axis=1)

# Step 4: Standardize Column Names (optional, if needed)
data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')
print("Columns after standardization:", data.columns)

# Step 5: Scale Numerical Columns
# MinMax Scaling to normalize all numerical values between 0 and 1
scaler = MinMaxScaler()
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
data[numerical_columns] = scaler.fit_transform(data[numerical_columns])

# Step 6: Save Cleaned Data to a New CSV File
data.to_csv('cleaned_data-final.csv', index=False)
print("Data has been cleaned and saved to 'cleaned_data-final.csv'")
