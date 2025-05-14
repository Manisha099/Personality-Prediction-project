import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor

# Step 1: Load the datasets
X_train = pd.read_csv('X_train_sampled.csv')
X_test = pd.read_csv('X_test_sampled.csv')
y_train = pd.read_csv('y_train_sampled.csv')
y_test = pd.read_csv('y_test_sampled.csv')

# Step 2: Analyze Correlations
print("\nAnalyzing Correlation Between Features and Targets...")
combined_data = pd.concat([X_train, y_train], axis=1)
correlation_matrix = combined_data.corr()

# Extract correlations between features and targets
correlation_with_targets = correlation_matrix.loc[X_train.columns, y_train.columns]
print("\nCorrelation Between Features and Targets:")
print(correlation_with_targets)

# Plot the heatmap for visualization
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_with_targets, annot=False, cmap='coolwarm', cbar=True)
plt.title('Feature-Target Correlation Heatmap')
plt.show()

# Step 3: Identify Irrelevant Features Automatically
threshold = 0.05
relevant_features = correlation_with_targets[correlation_with_targets.abs().max(axis=1) > threshold].index.tolist()

print("\nFeatures retained based on correlation threshold (>|0.05|):")
print(relevant_features)

# Drop irrelevant features from training and testing sets
X_train_reduced = X_train[relevant_features]
X_test_reduced = X_test[relevant_features]

# Step 4: Add Interaction Terms
print("\nAdding interaction terms...")
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_train_poly = poly.fit_transform(X_train_reduced)
X_test_poly = poly.transform(X_test_reduced)

print("Shape after adding interaction terms (train):", X_train_poly.shape)

# Step 5: Train and Evaluate Random Forest Model with Interaction Terms
print("\nTraining Random Forest Model with Interaction Terms...")
rf_model = MultiOutputRegressor(RandomForestRegressor(
    random_state=42, n_estimators=200, max_depth=10
))
rf_model.fit(X_train_poly, y_train)

# Predict and evaluate
rf_y_pred = rf_model.predict(X_test_poly)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_y_pred, multioutput='raw_values'))
rf_r2 = r2_score(y_test, rf_y_pred, multioutput='uniform_average')

print("\nRandom Forest Results with Interaction Terms:")
print("Root Mean Squared Error (per trait):", rf_rmse)
print("R² Score (overall):", rf_r2)

# Step 6: Train and Evaluate XGBoost Model
print("\nTraining XGBoost Model...")
xgb_model = MultiOutputRegressor(XGBRegressor(
    random_state=42, n_estimators=300, max_depth=10, learning_rate=0.1
))
xgb_model.fit(X_train_reduced, y_train)

# Predict and evaluate
xgb_y_pred = xgb_model.predict(X_test_reduced)
xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_y_pred, multioutput='raw_values'))
xgb_r2 = r2_score(y_test, xgb_y_pred, multioutput='uniform_average')

print("\nXGBoost Results:")
print("Root Mean Squared Error (per trait):", xgb_rmse)
print("R² Score (overall):", xgb_r2)

# Step 7: Analyze Target Variables
print("\nAnalyzing target variable distributions...")
y_train.describe()
y_train.hist(bins=20, figsize=(12, 8))
plt.suptitle("Target Variable Distributions")
plt.show()
