import pandas as pd
import pickle
import matplotlib.pyplot as plt
import warnings
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.sm_exceptions import ConvergenceWarning

# Ignore convergence warnings
warnings.simplefilter('ignore', ConvergenceWarning)

# Load your dataset
data = pd.read_csv('train.csv')

# Convert the 'Order Date' column to datetime
data['Order Date'] = pd.to_datetime(data['Order Date'], format='mixed')

# Set the 'Order Date' column as the index
data.set_index('Order Date', inplace=True)

# Resample the data to monthly frequency, summing up sales for each month
monthly_sales = data['Sales'].resample('ME').sum()

# Fit the SARIMAX model
model = SARIMAX(monthly_sales, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
results = model.fit()

# Save the model
with open('trained_model.pkl', 'wb') as f:
    pickle.dump(results, f)

# Predict the next 12 months (or any desired number of steps)
forecast_steps = 12
forecast = results.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=monthly_sales.index[-1] + pd.DateOffset(months=1), periods=forecast_steps, freq='M')
forecast_series = pd.Series(forecast.predicted_mean, index=forecast_index)

# Plot the original data and forecasted data
plt.figure(figsize=(10, 5))
plt.plot(monthly_sales, label='Observed Sales')
plt.plot(forecast_series, label='Forecasted Sales', color='red')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.title('Sales Forecast')
plt.legend()
plt.show()
