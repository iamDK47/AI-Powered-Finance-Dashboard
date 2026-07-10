import requests
# import datetime from datetime
import json
import os
from dotenv import load_dotenv
load_dotenv()
import time

beta_API = {'bitcoin' : {'usd' : 69420.96}}
Mock_API = False

coins = ['BTCUSDT,ETHUSDT,SOLUSDT,ADAUSDT,XRPUSDT']
result = ','.join(coins)

# The_url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=500"
The_url = "https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=5000"


while True:
  try:

    if Mock_API:
      mock_result = beta_API['bitcoin']['usd']
      print(f"BETA API WORKING price is ${mock_result:,}")
      print()

    else:
      # response = requests.get(The_url, headers=custom_header)
      response = requests.get(The_url)

      if response.status_code == 200:
        print("api is working")
        with open('response.json', 'w') as f:
          json.dump(response.json(), f, indent=2)
          # json.dump([response.json(),dict(response.headers), int(response.status_code)], f, indent=2)

      elif response.status_code == 429:
        retry_time = int(response.headers.get('Retry-After'))
        print("STOOOOOOOP!!!!!!!")
        print(f"try after {retry_time}")
        time.sleep(retry_time)
        continue

      else:  
        print("failed to connect")
        print(response.text)
        

  except Exception as err:
    print(f"error caught: {err}")
    

# for time intervals
# for TS,P in btc_price['prices']:
#   dt = datetime.fromtimestamp(TS/1000).strftime("%Y-%m-%d %H:%M:%S")
#   new_prices.append((dt,P))


