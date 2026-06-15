import requests
import os

beta_API = {'bitcoin' : {'usd' : 69420.96}}
Mock_API = False

coins = ['bitcoin,ethereum,solana,cardano,ripple']
result = ','.join(coins)

# The_url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids={result}"
# The_url = "https://api.coingecko.com/api/v3/search?query=bitcoin"
# The_url = "https://api.coingecko.com/api/v3/coins/list"
# The_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin&names=Bitcoin&symbols=btc&category=layer-1&price_change_percentage=1h"
# The_url = "https://api.coingecko.com/api/v3/coins/bitcoin"
The_url = "https://api.coingecko.com/api/v3/coins/bitcoin/tickers?exchange_ids=bybit"
# The_url = "https://api.coingecko.com/api/v3/coins/bitcoin/history?date=30-12-2023"
# The_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=1"
# The_url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from=1711929600&to=1712275200"
# The_url = "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc?vs_currency=usd"

custom_header = {
 "x-cg-demo-api-key": os.getenv('API_KEY')
}

try:

  if Mock_API:
    mock_result = beta_API['bitcoin']['usd']
    print(f"BETA API WORKING price is ${mock_result:,}")
    print()

  else:
    response = requests.get(The_url, headers=custom_header)

    if response.status_code == 200:
      print("api is working")
      response_json = response.json()
      print(response_json)

    else:  
      print("failed to connect")
      print(response.text)

except Exception as err:
  print(f"error caught: {err}")