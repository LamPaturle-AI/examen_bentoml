import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load raw data
df = pd.read_csv("data/raw/admission.csv", index_col='Serial No.')

# Separate features (X) and target (y)
X = df.drop("Chance of Admit ", axis=1)
y = df["Chance of Admit "]

# Train-test split
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=0.2, random_state=42) 

# Save preprocessed data
X_train.to_csv("data/processed/X_train.csv", index=False)
X_test.to_csv("data/processed/X_test.csv", index=False)
y_train.to_csv("data/processed/y_train.csv", index=False)
y_test.to_csv("data/processed/y_test.csv", index=False)

print("4 datasets X_train.csv, X_test.csv, y_train.csv and y_test.csv saved to data/processed.")

# Initialize scaler
scaler = StandardScaler()

# Normalize (fit on X_train, then transform both X_train and X_test)
X_train_scaled_array = scaler.fit_transform(X_train)
X_test_scaled_array = scaler.transform(X_test)

# Convert NumPy arrays back to DataFrames, preserving original column names
X_train_scaled = pd.DataFrame(X_train_scaled_array, columns=X_train.columns)
X_test_scaled = pd.DataFrame(X_test_scaled_array, columns=X_test.columns)

# Write resulting normalized sets to CSV
X_train_scaled.to_csv("data/processed/X_train_scaled.csv", index=False)
X_test_scaled.to_csv("data/processed/X_test_scaled.csv", index=False)

print("2 normalized datasets X_train_scaled.csv and X_test_scaled.csv saved to data/processed.")