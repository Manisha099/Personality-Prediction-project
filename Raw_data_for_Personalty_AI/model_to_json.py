from sklearn.ensemble import RandomForestRegressor
import json
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load models from JSON
with open('models.json', 'r') as json_file:
    json_models = json.load(json_file)

# Load scaler from JSON
with open('scaler.json', 'r') as scaler_file:
    scaler_params = json.load(scaler_file)

# Reconstruct scaler
scaler = StandardScaler()
scaler.mean_ = np.array(scaler_params["mean"])
scaler.scale_ = np.array(scaler_params["scale"])

# Reconstruct models
models = {}
for trait, params in json_models.items():
    model = RandomForestRegressor(
        n_estimators=params["n_estimators"],
        max_depth=params["max_depth"],
        min_samples_split=params["min_samples_split"],
        min_samples_leaf=params["min_samples_leaf"],
        bootstrap=params["bootstrap"],
        random_state=42
    )
    models[trait] = model

print("Models and scaler loaded successfully!")
