import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

# Step 1: Load the datasets
X_train = pd.read_csv('X_train_sampled.csv')
X_test = pd.read_csv('X_test_sampled.csv')
y_train = pd.read_csv('y_train_sampled.csv')
y_test = pd.read_csv('y_test_sampled.csv')

# Step 2: Analyze Target Distributions
print("Analyzing target variable distributions...")
y_train.hist(bins=20, figsize=(12, 8))
plt.suptitle('Distribution of Target Variables (OCEAN traits)')
plt.show()

# Step 3: Normalize the Features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 4: Train and Evaluate Random Forest (Baseline Model)
print("\nTraining Random Forest (Baseline Model)...")
rf_model = MultiOutputRegressor(RandomForestRegressor(
    random_state=42, n_estimators=200, max_depth=20, min_samples_split=5
))
rf_model.fit(X_train_scaled, y_train)
rf_y_pred = rf_model.predict(X_test_scaled)

# Evaluate the Random Forest model
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_y_pred, multioutput='raw_values'))
rf_r2 = r2_score(y_test, rf_y_pred, multioutput='uniform_average')

print("\nRandom Forest Results:")
print("Root Mean Squared Error (per trait):", rf_rmse)
print("R² Score (overall):", rf_r2)

# Step 5: Feature Importance from Random Forest
print("\nFeature Importance (Random Forest):")
rf_importances = rf_model.estimators_[0].feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': rf_importances
}).sort_values(by='Importance', ascending=False)
print(feature_importance_df)

# Step 6: Remove Less Important Features
print("\nRetaining only important features for training...")
important_features = ['ext1', 'ext6', 'ext8', 'ext4', 'ext5', 'ext7', 'ext10']
X_train_reduced = X_train[important_features]
X_test_reduced = X_test[important_features]

# Step 7: Retrain Random Forest with Reduced Features
print("\nRetraining Random Forest with Reduced Features...")
rf_reduced_model = MultiOutputRegressor(RandomForestRegressor(
    random_state=42, n_estimators=200, max_depth=20, min_samples_split=5
))
rf_reduced_model.fit(X_train_reduced, y_train)
rf_reduced_y_pred = rf_reduced_model.predict(X_test_reduced)

# Evaluate the reduced Random Forest model
rf_reduced_rmse = np.sqrt(mean_squared_error(y_test, rf_reduced_y_pred, multioutput='raw_values'))
rf_reduced_r2 = r2_score(y_test, rf_reduced_y_pred, multioutput='uniform_average')

print("\nRandom Forest (Reduced Features) Results:")
print("Root Mean Squared Error (per trait):", rf_reduced_rmse)
print("R² Score (overall):", rf_reduced_r2)

# Step 8: Train and Evaluate XGBoost
print("\nTraining XGBoost Model...")
xgb_model = MultiOutputRegressor(XGBRegressor(
    random_state=42, n_estimators=200, max_depth=10, learning_rate=0.1
))
xgb_model.fit(X_train_scaled, y_train)
xgb_y_pred = xgb_model.predict(X_test_scaled)

# Evaluate the XGBoost model
xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_y_pred, multioutput='raw_values'))
xgb_r2 = r2_score(y_test, xgb_y_pred, multioutput='uniform_average')

print("\nXGBoost Results:")
print("Root Mean Squared Error (per trait):", xgb_rmse)
print("R² Score (overall):", xgb_r2)
