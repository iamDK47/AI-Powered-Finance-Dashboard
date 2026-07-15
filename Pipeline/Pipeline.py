# import psycopg2
# import os
from dotenv import load_dotenv
# import datetime from datetime
load_dotenv()
from pipelineExc import fetch_klines

coins = ['BTCUSDT','ETHUSDT','BNBUSDT','XRPUSDT','SOLUSDT','TRXUSDT','DOGEUSDT','XLMUSDT','ZECUSDT','ADAUSDT','LINKUSDT','GRAMUSDT','DEXEUSDT','LTCUSDT','HBARUSDT','UNIUSDT','SUIUSDT','AVAXUSDT','SHIBUSDT','NEARUSDT']

fetch_klines(coins)
# conn = psycopg2.connect(
#     host="localhost",
#     dbname="Crypto_Analytics",
#     user="postgres",
#     password = os.getenv("DB_Password"),
#     port=5432
# )

# All_data = twenty_coins(coins)


# cur = conn.cursor()

# cur.execute("""
#             INSERT INTO global_crypto_data (ticker,open,high,low,close,volume_COIN,volume_USDT,total_trades,market_buyer_volume,market_sell_volume,delta,close_Time)
#             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#             ()
#             """)

# conn.commit()
# cur.close()
# conn.close()

# [
#   {
#     "ticker": "BTCUSDT",
#     "data": [
#       1784030820000,
#       "62806.58000000",
#       "62808.00000000",
#       "62799.40000000",
#       "62807.99000000",
#       "24.08440000",
#       1784030879999,
#       "1512580.67078600",
#       2081,
#       "10.24250000",
#       "643260.06636650",
#       "0"
#     ]
#   },
# ]














# for time intervals
# for TS,P in btc_price['prices']:
#   dt = datetime.fromtimestamp(TS/1000).strftime("%Y-%m-%d %H:%M:%S")
#   new_prices.append((dt,P))


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


# url = 'https://api.binance.com/api/v3/ticker/24hr'

# try:

#   if Mock_API:
#     mock_result = beta_API['bitcoin']['usd']
#     print(f"BETA API WORKING price is ${mock_result:,}")
#     print()

#   else:

#       response = requests.get(url)

#       if response.status_code == 200:
#         print("api is working")
#         All_data.append(response.json())
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
