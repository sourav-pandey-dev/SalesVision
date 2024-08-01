from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)
CORS(app)

# Load the dataset
file_path = 'train.csv'
data = pd.read_csv(file_path)

# Convert Order Date to datetime
data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y')

# Load the trained model
with open('trained_model.pkl', 'rb') as f:
    trained_model = pickle.load(f)

@app.route('/products', methods=['GET'])
def get_products():
    products = data['Product'].unique().tolist()
    return jsonify({'products': products})

@app.route('/forecast', methods=['POST'])
def forecast():
    req_data = request.json
    product = req_data.get('product')
    
    # Filter the data for the selected product
    product_data = data[data['Product'] == product]
    product_data.set_index('Order Date', inplace=True)
    product_data.index = pd.to_datetime(product_data.index, format='%d/%m/%Y')
    monthly_sales = product_data['Sales'].resample('ME').sum()
    
    # Fill missing values if any
    monthly_sales = monthly_sales.fillna(0)

    # Fit the model on the filtered data
    model = SARIMAX(monthly_sales, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    result = model.fit(disp=False)
    
    # Forecast future sales
    forecast = result.get_forecast(steps=12)
    forecast_mean = forecast.predicted_mean
    forecast_conf_int = forecast.conf_int()

    past_sales = monthly_sales.reset_index().rename(columns={'Order Date': 'date', 'Sales': 'sales'}).to_dict(orient='records')
    forecast_mean = forecast_mean.reset_index().rename(columns={'index': 'date', 'predicted_mean': 'sales'}).to_dict(orient='records')
    forecast_conf_int = forecast_conf_int.reset_index().rename(columns={'index': 'date', 0: 'lower', 1: 'upper'}).to_dict(orient='records')

    response = {
        'past_sales': past_sales,
        'forecast_mean': forecast_mean,
        'forecast_conf_int': forecast_conf_int
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
