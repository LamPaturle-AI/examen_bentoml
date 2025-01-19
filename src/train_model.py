import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import numpy as np
import bentoml

# Load training data
X_train = pd.read_csv('data/processed/X_train_scaled.csv')
y_train = pd.read_csv('data/processed/y_train.csv').squeeze()

# Define parameter grid for GradientBoostingRegressor
param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, 10],
    "learning_rate": [0.01, 0.1, 0.2]
}

# Initialize regression model
model = GradientBoostingRegressor(random_state=42)

# Set up GridSearchCV
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring="neg_mean_squared_error",  # or "r2", "neg_mean_absolute_error", etc.
    cv=5,              # 5-fold cross-validation
    n_jobs=-1,         # use all available CPU cores
    verbose=1          # print progress messages
)

# Fit grid search on training data
grid_search.fit(X_train, y_train)

# Create model with best parameters
gbr = GradientBoostingRegressor(random_state=42, **grid_search.best_params_)

# Train model
gbr.fit(X_train, y_train)

# Load test data
X_test = pd.read_csv('data/processed/X_test_scaled.csv')
y_test = pd.read_csv("data/processed/y_test.csv").squeeze()

# Test model
y_pred = gbr.predict(X_test)

# Get model accuracy
accuracy = gbr.score(X_test, y_test)

print(f"Model accuracy: {accuracy}")

# Test model on single observation
test_data = X_test.iloc[[0]]
# Print actual label
print(f"Actual label: {y_test[0]}")
# Print predicted label
print(f"Predicted label: {gbr.predict(test_data)[0]}")

# Evaluate model
mse = mean_squared_error(y_test,y_pred)
rmse = np.sqrt(mse)

print(f"Model RMSE: {rmse}")

# Save model in BentoML Model Store
model_gbr = bentoml.sklearn.save_model("admissions_gbr", gbr)

print(f"Model trained successfully and saved as : {model_gbr}")