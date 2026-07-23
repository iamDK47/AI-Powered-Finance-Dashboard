import requests
import json
import time
from pipeline_func import exchange_info_instrument
# from pipeline_func import fetch_klines
# from database import load_kline
from pipeline_func import fetch_24h_tickers
# from database import load_corr_cov
# import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
import numpy as np
import pandas as pd
   

ticker_by_price, ticker_by_volume, transformed_price_chg, transformed_vol_chg = fetch_24h_tickers()

transformed_dict = exchange_info_instrument(ticker_by_price)


# conn = psycopg2.connect(
#         host="localhost",
#         dbname="Crypto_Analytics",
#         user="postgres",
#         password = os.getenv("DB_Password"),
#         port=5432
#     )

# all_data = fetch_klines(ticker_by_volume)

# load_kline(all_data, conn)

# load_corr_cov(top_300price_chg, conn)

# conn.commit()
# conn.close()

#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# url = 'https://api.binance.com/api/v3/ticker/24hr'
# url = 'https://api.binance.com/api/v3/exchangeInfo'

# all_data = []

# try:

#       response = requests.get(url)

#       if response.status_code == 200:
#         print("api is working")
#         all_data.append(response.json())
#         print(len(all_data[0]))

#         # coin = next( c for c in response.json() if c['symbol'] == 'EOSUPUSDT' )
#         # print(coin)
#         with open('response.json', 'w') as f:
#         #   json.dump([response.json(),dict(response.headers), int(response.status_code)], f, indent=2)
#           json.dump(response.json(), f, indent=2)
        
#       elif response.status_code == 429:
#         retry_time = int(response.headers.get('Retry-After'))
#         print("STOOOOOOOP!!!!!!!")
#         print(f"try after {retry_time}")
#         time.sleep(retry_time)

#       else:
#         print("failed to connect")
#         print(response.text)

# except Exception as err:
#   print(f"error caught: {err}")