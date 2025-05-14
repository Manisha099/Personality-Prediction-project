import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Load data
file_path = 'cleaned_sampled_100k_data.csv'
data = pd.read_csv(file_path)

# Sample and filter necessary columns
sampled_data = data.sample(n=1000, random_state=42)
ocean_columns = [
    'ext1', 'ext2', 'ext3', 'ext4', 'ext5', 'agr1', 'agr2', 'agr3', 'agr4', 'agr5',
    'opn1', 'opn2', 'opn3', 'opn4', 'opn5', 'csn1', 'csn2', 'csn3', 'csn4', 'csn5',
    'est1', 'est2', 'est3', 'est4', 'est5'
]
sampled_data = sampled_data[ocean_columns]

# Compute OCEAN traits
sampled_data['Extraversion'] = sampled_data[['ext1', 'ext2', 'ext3', 'ext4', 'ext5']].mean(axis=1)
sampled_data['Agreeableness'] = sampled_data[['agr1', 'agr2', 'agr3', 'agr4', 'agr5']].mean(axis=1)
sampled_data['Openness'] = sampled_data[['opn1', 'opn2', 'opn3', 'opn4', 'opn5']].mean(axis=1)
sampled_data['Conscientiousness'] = sampled_data[['csn1', 'csn2', 'csn3', 'csn4', 'csn5']].mean(axis=1)
sampled_data['Neuroticism'] = sampled_data[['est1', 'est2', 'est3', 'est4', 'est5']].mean(axis=1)

# Features and targets
X = sampled_data[ocean_columns]
y = sampled_data[['Extraversion', 'Agreeableness', 'Openness', 'Conscientiousness', 'Neuroticism']]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train and save models as JSON
models = {}
json_models = {}

for trait in y.columns:
    # Train model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train_scaled, y_train[trait])

    # Save model parameters to JSON-compatible format
    json_models[trait] = {
        "n_estimators": model.n_estimators,
        "max_depth": model.max_depth,
        "min_samples_split": model.min_samples_split,
        "min_samples_leaf": model.min_samples_leaf,
        "bootstrap": model.bootstrap,
        "feature_importances_": model.feature_importances_.tolist()
    }

# Save JSON models and scaler
with open('models.json', 'w') as json_file:
    json.dump(json_models, json_file)

# Save scaler separately as JSON
scaler_params = {
    "mean": scaler.mean_.tolist(),
    "scale": scaler.scale_.tolist()
}
with open('scaler.json', 'w') as scaler_file:
    json.dump(scaler_params, scaler_file)
