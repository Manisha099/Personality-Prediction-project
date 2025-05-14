import pandas as pd
from sklearn.model_selection import train_test_split

# Load your dataset
file_path = 'cleaned_sampled_100k_data.csv'  # Update the file path if necessary
data = pd.read_csv(file_path)

# Split the data into features (X) and labels/targets (y)
# Assuming the first 10 columns are input features and the rest are target variables
X = data.iloc[:, :10]  # First 10 columns as features
y = data.iloc[:, 10:]  # Remaining columns as target variables

# Perform an 80/20 train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save the splits locally as CSV files
X_train.to_csv('X_train.csv', index=False)
X_test.to_csv('X_test.csv', index=False)
y_train.to_csv('y_train.csv', index=False)
y_test.to_csv('y_test.csv', index=False)

print("Train-test split completed and saved as CSV files.")
