#02UFWIM2I3UK5Y9N
import pandas as pd
import requests

# Define the Alpha Vantage API endpoint and parameters
api_url = "https://www.alphavantage.co/query"
api_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "outputsize": "full",
    "apikey": "02UFWIM2I3UK5Y9N"
}

# Initialize an empty list of stocks
stocks = []

# Define the moving average window sizes
short_window = 50
long_window = 200

# Handle form submission
@app.route('/add_stock', methods=['POST'])
def add_stock():
    stock_symbol = request.form['stock_symbol'].upper()

    # Update the API parameters with the user's input
    api_params['symbol'] = stock_symbol

    # Send the API request and retrieve the response data
    response = requests.get(api_url, api_params)
    response_json = response.json()

    # Convert the response data to a pandas DataFrame
    stock_df = pd.DataFrame.from_dict(response_json['Time Series (Daily)'], orient='index')
    stock_df.index = pd.to_datetime(stock_df.index)
    stock_df.columns = ['open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend_amount', 'split_coefficient']
    stock_df = stock_df.astype(float)

    # Calculate the moving averages
    stock_df['short_mavg'] = stock_df['close'].rolling(window=short_window).mean()
    stock_df['long_mavg'] = stock_df['close'].rolling(window=long_window).mean()

    # Generate buy and sell signals
    stock_df['signal'] = 0.0
    stock_df['signal'][short_window:] = np.where(stock_df['short_mavg'][short_window:] > stock_df['long_mavg'][short_window:], 1.0, 0.0)
    stock_df['positions'] = stock_df['signal'].diff()

    # Convert the DataFrame back to a Plotly-friendly format
    stock_data = {
        'x': stock_df.index,
        'y': stock_df['close'],
        'type': 'scatter',
        'mode': 'lines',
        'name': stock_symbol
    }
    stocks.append(stock_data)

    # Plot the stock price data using Plotly
    layout = {
        'title': 'Stock Price Comparison',
        'xaxis': {'title': 'Date'},
        'yaxis': {'title': 'Price'}
    }
    fig = go.Figure(data=stocks, layout=layout)
    plot_div = plot(fig, output_type='div')

    # Determine whether to recommend buying or selling the stock
    if stock_df['positions'][-1] == 1.0:
        recommendation = 'BUY'
    elif stock_df['positions'][-1] == -1.0:
        recommendation = 'SELL'
    else:
        recommendation = 'HOLD'

