import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from joblib import dump
import os
import datetime

# Load your CSV file
file_path = os.path.join('myapp', 'data', 'market_prices.csv')
df = pd.read_csv(file_path)

# Clean column names (remove leading/trailing spaces)
df.columns = df.columns.str.strip()

# Ensure required column exists
if 'Price Date' not in df.columns:
    raise KeyError("The column 'Price Date' is missing. Check the CSV header.")

# Drop rows with missing values
df.dropna(inplace=True)

# Parse date
try:
    df['Date'] = pd.to_datetime(df['Price Date'], format='%d-%b-%y')
except Exception as e:
    raise ValueError(f"Error parsing 'Price Date': {e}")

# Feature Engineering
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Weekday'] = df['Date'].dt.weekday

# Select features and target
categorical_cols = ['District Name', 'State', 'Market Name', 'Commodity', 'Variety']
X = df[['Month', 'Day', 'Weekday']].join(df[categorical_cols])
X = pd.get_dummies(X, drop_first=True)

# Target variable
if 'Modal Price (Rs./Quintal)' not in df.columns:
    raise KeyError("Target column 'Modal Price (Rs./Quintal)' is missing in the data.")
y = df['Modal Price (Rs./Quintal)']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluate model (optional)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Model trained. Test MSE: {mse:.2f}")

# Save model and column info
model_dir = os.path.join('myapp', 'ai_model')
os.makedirs(model_dir, exist_ok=True)
dump((model, X.columns), os.path.join(model_dir, 'price_predictor.joblib'))

print("✅ Model trained and saved successfully!")

