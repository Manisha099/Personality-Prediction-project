import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
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

# Step 3: Transform and Scale Target Variables
print("\nApplying Log Transformation to Target Variables...")
y_train_transformed = np.log1p(y_train)
y_test_transformed = np.log1p(y_test)

print("\nScaling Target Variables...")
scaler = StandardScaler()
y_train_scaled = scaler.fit_transform(y_train_transformed)
y_test_scaled = scaler.transform(y_test_transformed)

# Step 4: Add Interaction Terms
print("\nAdding interaction terms...")
poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

# Step 5: Train Random Forest with Interaction Terms
print("\nTraining Random Forest Model...")
rf_model = MultiOutputRegressor(RandomForestRegressor(
    random_state=42, n_estimators=200, max_depth=10
))
rf_model.fit(X_train_poly, y_train_scaled)

# Predict and evaluate
rf_y_pred = rf_model.predict(X_test_poly)
rf_rmse = np.sqrt(mean_squared_error(y_test_scaled, rf_y_pred, multioutput='raw_values'))
rf_r2 = r2_score(y_test_scaled, rf_y_pred, multioutput='uniform_average')

print("\nRandom Forest Results with Transformed Targets:")
print("Root Mean Squared Error (per trait):", rf_rmse)
print("R² Score (overall):", rf_r2)

# Step 6: Train XGBoost
print("\nTraining XGBoost Model...")
xgb_model = MultiOutputRegressor(XGBRegressor(
    random_state=42, n_estimators=300, max_depth=10, learning_rate=0.1
))
xgb_model.fit(X_train, y_train_scaled)

# Predict and evaluate
xgb_y_pred = xgb_model.predict(X_test)
xgb_rmse = np.sqrt(mean_squared_error(y_test_scaled, xgb_y_pred, multioutput='raw_values'))
xgb_r2 = r2_score(y_test_scaled, xgb_y_pred, multioutput='uniform_average')

print("\nXGBoost Results with Transformed Targets:")
print("Root Mean Squared Error (per trait):", xgb_rmse)
print("R² Score (overall):", xgb_r2)

# Step 7: Train Neural Network
print("\nTraining Neural Network...")
nn_model = Sequential([
    Dense(128, input_dim=X_train.shape[1], activation='relu'),
    Dense(64, activation='relu'),
    Dense(y_train_scaled.shape[1], activation='linear')
])
nn_model.compile(optimizer='adam', loss='mse', metrics=['mae'])

nn_model.fit(X_train, y_train_scaled, epochs=50, batch_size=32, validation_data=(X_test, y_test_scaled))

# Predict and evaluate
nn_y_pred = nn_model.predict(X_test)
nn_rmse = np.sqrt(mean_squared_error(y_test_scaled, nn_y_pred, multioutput='raw_values'))
nn_r2 = r2_score(y_test_scaled, nn_y_pred, multioutput='uniform_average')

print("\nNeural Network Results with Transformed Targets:")
print("Root Mean Squared Error (per trait):", nn_rmse)
print("R² Score (overall):", nn_r2)
