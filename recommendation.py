import requests

def get_stock_data(symbol):
    # Define the Alpha Vantage API endpoint and parameters
    api_url = "https://www.alphavantage.co/query"
    api_params = {
      "function": "TIME_SERIES_DAILY_ADJUSTED",
      "outputsize": "compact",
      "symbol": symbol,
      "apikey": "02UFWIM2I3UK5Y9N"
    }

    # Send the API request and retrieve the response data
    response = requests.get(api_url, params=api_params).json()

    # Extract the latest closing price from the response data
    latest_date = list(response["Time Series (Daily)"].keys())[0]
    latest_price = float(response["Time Series (Daily)"][latest_date]["4. close"])

    # Determine the recommendation based on the latest closing price
    if latest_price < 50:
        return "BUY"
    elif latest_price > 100:
        return "SELL"
    else:
        return "HOLD"
