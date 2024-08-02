from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

app = Flask(__name__)
CORS(app)

@app.route('/categories', methods=['GET'])
def categories():
    try:
        # Load the dataset
        data = pd.read_csv('train.csv')

        # Extract unique categories
        categories = data['Category'].unique().tolist()

        # Return the categories as JSON
        return jsonify({'categories': categories})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/forecast', methods=['POST'])
def forecast():
    try:
        # Load the request data
        data = request.get_json()
        category = data['category']

        # Load the dataset
        df = pd.read_csv('train.csv')

        # Filter data by the selected category
        df = df[df['Category'] == category]

        # Ensure Order Date is datetime
        df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')

        # Ensure Sales column is numeric
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

        # Drop rows with missing Sales values
        df.dropna(subset=['Sales'], inplace=True)

        # Aggregate sales data by month
        df.set_index('Order Date', inplace=True)
        monthly_sales = df['Sales'].resample('ME').sum()

        if monthly_sales.empty:
            return jsonify({'error': 'No data available for the selected category'})

        # Fit the SARIMA model
        model = SARIMAX(monthly_sales, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        result = model.fit()

        # Define the number of steps to forecast (e.g., 12 months)
        forecast_steps = int(request.args.get('steps', 12))

        # Make future predictions
        future_predictions = result.get_forecast(steps=forecast_steps)
        predicted_sales = future_predictions.predicted_mean

        past_sales = monthly_sales.reset_index().rename(columns={'Order Date': 'date', 'Sales': 'sales'}).to_dict(orient='records')
        forecast_mean = predicted_sales.reset_index().rename(columns={'index': 'date', 'predicted_mean': 'sales'}).to_dict(orient='records')
        forecast_conf_int = future_predictions.conf_int().reset_index().rename(columns={'index': 'date'}).to_dict(orient='records')

        # Return the predictions as JSON
        return jsonify({
            'past_sales': past_sales,
            'forecast_mean': forecast_mean,
            'forecast_conf_int': forecast_conf_int
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
