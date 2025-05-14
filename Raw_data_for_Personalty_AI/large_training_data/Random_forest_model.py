import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load the train and test datasets
X_train = pd.read_csv('X_train.csv')
X_test = pd.read_csv('X_test.csv')
y_train = pd.read_csv('y_train.csv')
y_test = pd.read_csv('y_test.csv')

# Initialize the Random Forest Regressor for multi-output regression
model = MultiOutputRegressor(RandomForestRegressor(random_state=42))

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model
rmse = np.sqrt(mean_squared_error(y_test, y_pred, multioutput='raw_values'))
r2 = r2_score(y_test, y_pred, multioutput='uniform_average')

# Display the evaluation metrics
print("Root Mean Squared Error (per trait):", rmse)
print("R² Score (overall):", r2)
