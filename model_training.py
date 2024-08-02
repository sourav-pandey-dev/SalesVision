import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pickle
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the dataset
file_path = 'train.csv'  # Adjust this path as needed
data = pd.read_csv(file_path)

# Convert Order Date to datetime
data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y')

# Ensure Sales column is numeric
data['Sales'] = pd.to_numeric(data['Sales'], errors='coerce')

# Drop rows with missing Sales values
data.dropna(subset=['Sales'], inplace=True)

# Aggregate sales data by month
data.set_index('Order Date', inplace=True)
monthly_sales = data['Sales'].resample('ME').sum()

# Check the number of observations
if len(monthly_sales) < 24:  # Arbitrary threshold, adjust as needed
    logging.warning("Too few observations to fit the seasonal ARIMA model accurately.")

# Fit the SARIMA model
try:
    model = SARIMAX(monthly_sales, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    result = model.fit()
    logging.info("Model fitting completed successfully.")
except Exception as e:
    logging.error(f"Model fitting failed: {e}")
    raise

# Save the trained model
with open('trained_model.pkl', 'wb') as f:
    pickle.dump(result, f)
    logging.info("Model saved successfully.")
