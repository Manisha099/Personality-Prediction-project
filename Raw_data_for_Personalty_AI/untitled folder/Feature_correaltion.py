import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the datasets
X_train = pd.read_csv('X_train_sampled.csv')
y_train = pd.read_csv('y_train_sampled.csv')

# Combine the features and targets for correlation analysis
combined_data = pd.concat([X_train, y_train], axis=1)

# Calculate the correlation matrix
correlation_matrix = combined_data.corr()

# Extract correlations of features with target variables only
correlation_with_targets = correlation_matrix.loc[X_train.columns, y_train.columns]

# Display the correlations
print("\nCorrelation Between Features and Targets:")
print(correlation_with_targets)

# Plot the heatmap for better visualization
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_with_targets, annot=True, cmap='coolwarm', fmt=".2f", cbar=True)
plt.title('Feature-Target Correlation Heatmap')
plt.show()
