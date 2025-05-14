import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load the datasets
X_train = pd.read_csv('X_train_sampled.csv')
X_test = pd.read_csv('X_test_sampled.csv')
y_train = pd.read_csv('y_train_sampled.csv')
y_test = pd.read_csv('y_test_sampled.csv')

# Step 2: Analyze Target Variable Distributions
print("\nAnalyzing Target Variable Distributions...")
y_train.describe()
y_train.hist(bins=20, figsize=(12, 8))
plt.suptitle("Target Variable Distributions")
plt.show()

# Apply Log Transformation (if needed for skewed data)
print("\nApplying Log Transformation to Target Variables...")
y_train_transformed = np.log1p(y_train)  # log1p handles log(0) safely
y_test_transformed = np.log1p(y_test)

# Step 3: Analyze Correlations
print("\nAnalyzing Correlation Between Features and Transformed Targets...")
combined_data = pd.concat([X_train, y_train_transformed], axis=1)
correlation_matrix = combined_data.corr()

# Extract correlations between features and targets
correlation_with_targets = correlation_matrix.loc[X_train.columns, y_train_transformed.columns]
print("\nCorrelation Between Features and Transformed Targets:")
print(correlation_with_targets)

# Plot the heatmap for visualization
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_with_targets, annot=False, cmap='coolwarm', cbar=True)
plt.title('Feature-Target Correlation Heatmap')
plt.show()

# Step 4: Identify Relevant Features
threshold = 0.05
relevant_features = correlation_with_targets[correlation_with_targets.abs().max(axis=1) > threshold].index.tolist()

print("\nFeatures retained based on correlation threshold (>|0.05|):")
print(relevant_features)

# Drop irrelevant features from training and testing sets
X_train_reduced = X_train[relevant_features]
X_test_reduced = X_test[relevant_features]

# Step 5: Add Interaction Terms
print("\nAdding interaction terms...")
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_train_poly = poly.fit_transform(X_train_reduced)
X_test_poly = poly.transform(X_test_reduced)

print("Shape after adding interaction terms (train):", X_train_poly.shape)

# Step 6: Train Random Forest with Interaction Terms
print("\nTraining Random Forest Model with Interaction Terms...")
rf_model = MultiOutputRegressor(RandomForestRegressor(
    random_state=42, n_estimators=200, max_depth=10
))
rf_model.fit(X_train_poly, y_train_transformed)

# Predict and evaluate
rf_y_pred = rf_model.predict(X_test_poly)
rf_rmse = np.sqrt(mean_squared_error(y_test_transformed, rf_y_pred, multioutput='raw_values'))
rf_r2 = r2_score(y_test_transformed, rf_y_pred, multioutput='uniform_average')

print("\nRandom Forest Results with Interaction Terms and Transformed Targets:")
print("Root Mean Squared Error (per trait):", rf_rmse)
print("R² Score (overall):", rf_r2)

# Step 7: Train XGBoost
print("\nTraining XGBoost Model...")
xgb_model = MultiOutputRegressor(XGBRegressor(
    random_state=42, n_estimators=300, max_depth=10, learning_rate=0.1
))
xgb_model.fit(X_train_reduced, y_train_transformed)

# Predict and evaluate
xgb_y_pred = xgb_model.predict(X_test_reduced)
xgb_rmse = np.sqrt(mean_squared_error(y_test_transformed, xgb_y_pred, multioutput='raw_values'))
xgb_r2 = r2_score(y_test_transformed, xgb_y_pred, multioutput='uniform_average')

print("\nXGBoost Results with Transformed Targets:")
print("Root Mean Squared Error (per trait):", xgb_rmse)
print("R² Score (overall):", xgb_r2)

# Step 8: Train Neural Network
print("\nTraining Neural Network...")
nn_model = Sequential([
    Dense(128, input_dim=X_train_reduced.shape[1], activation='relu'),
    Dense(64, activation='relu'),
    Dense(y_train.shape[1], activation='linear')
])
nn_model.compile(optimizer='adam', loss='mse', metrics=['mae'])

nn_model.fit(X_train_reduced, y_train_transformed, epochs=50, batch_size=32, validation_data=(X_test_reduced, y_test_transformed))

# Predict and evaluate
nn_y_pred = nn_model.predict(X_test_reduced)
nn_rmse = np.sqrt(mean_squared_error(y_test_transformed, nn_y_pred, multioutput='raw_values'))
nn_r2 = r2_score(y_test_transformed, nn_y_pred, multioutput='uniform_average')

print("\nNeural Network Results with Transformed Targets:")
print("Root Mean Squared Error (per trait):", nn_rmse)
print("R² Score (overall):", nn_r2)
