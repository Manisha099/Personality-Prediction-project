import pandas as pd

# Load the datasets
X_train = pd.read_csv('X_train.csv')
X_test = pd.read_csv('X_test.csv')
y_train = pd.read_csv('y_train.csv')
y_test = pd.read_csv('y_test.csv')

# Reduce the size of the datasets
# Adjust 'n' to set the number of rows you want in the smaller dataset
X_train_sampled = X_train.sample(n=10000, random_state=42)  # Reduce to 10,000 rows for training
y_train_sampled = y_train.loc[X_train_sampled.index]         # Match the sampled rows in y_train

X_test_sampled = X_test.sample(n=2000, random_state=42)      # Reduce to 2,000 rows for testing
y_test_sampled = y_test.loc[X_test_sampled.index]            # Match the sampled rows in y_test

# Save the reduced datasets as new CSV files
X_train_sampled.to_csv('X_train_sampled.csv', index=False)
y_train_sampled.to_csv('y_train_sampled.csv', index=False)
X_test_sampled.to_csv('X_test_sampled.csv', index=False)
y_test_sampled.to_csv('y_test_sampled.csv', index=False)

print("Reduced datasets saved as 'X_train_sampled.csv', 'y_train_sampled.csv', 'X_test_sampled.csv', 'y_test_sampled.csv'.")
