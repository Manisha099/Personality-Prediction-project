import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load the datasets
X_train = pd.read_csv('X_train_sampled.csv')
X_test = pd.read_csv('X_test_sampled.csv')
y_train = pd.read_csv('y_train_sampled.csv')
y_test = pd.read_csv('y_test_sampled.csv')

# Normalize the features using StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize the Random Forest Regressor for multi-output regression
model = MultiOutputRegressor(RandomForestRegressor(
    random_state=42,
    n_estimators=200,  # Increase number of trees
    max_depth=20,      # Set a maximum depth to avoid overfitting
    min_samples_split=5  # Minimum samples needed to split a node
))

# Train the model
model.fit(X_train_scaled, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test_scaled)

# Evaluate the model
rmse = np.sqrt(mean_squared_error(y_test, y_pred, multioutput='raw_values'))
r2 = r2_score(y_test, y_pred, multioutput='uniform_average')

# Display the evaluation metrics
print("Root Mean Squared Error (per trait):", rmse)
print("R² Score (overall):", r2)

# Feature Importance (for insights)
importances = model.estimators_[0].feature_importances_
feature_importance_df = pd.DataFrame({
    'Feature': X_train.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print("Feature Importances:")
print(feature_importance_df)
