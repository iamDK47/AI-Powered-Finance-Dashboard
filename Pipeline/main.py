import requests
import json
import time
from pipeline_func import fetch_klines
from database import load_kline
from pipeline_func import fetch_major_assets
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

ticker_by_price, ticker_by_volume, top_300price_chg, top_300vol_chg = fetch_major_assets()

conn = psycopg2.connect(
        host="localhost",
        dbname="Crypto_Analytics",
        user="postgres",
        password = os.getenv("DB_Password"),
        port=5432
    )

all_data = fetch_klines(ticker_by_price[:20])

load_kline(all_data, conn)


conn.commit()
conn.close()


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


# url = 'https://api.binance.com/api/v3/ticker/24hr'

# all_data = []

# try:

#       response = requests.get(url)

#       if response.status_code == 200:
#         print("api is working")
#         all_data.append(response.json())
#         print(len(all_data[0]))
#         with open('response.json', 'w') as f:
#           json.dump([response.json(),dict(response.headers), int(response.status_code)], f, indent=2)

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
