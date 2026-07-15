import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
from pipeline_func import fetch_klines
# import datetime from datetime

coins = ['BTCUSDT','ETHUSDT','BNBUSDT','XRPUSDT','SOLUSDT','TRXUSDT','DOGEUSDT','XLMUSDT','ZECUSDT','ADAUSDT','LINKUSDT','GRAMUSDT','DEXEUSDT','LTCUSDT','HBARUSDT','UNIUSDT','SUIUSDT','AVAXUSDT','SHIBUSDT','NEARUSDT']

all_data = fetch_klines(coins)

conn = psycopg2.connect(
    host="localhost",
    dbname="Crypto_Analytics",
    user="postgres",
    password = os.getenv("DB_Password"),
    port=5432
)

cur = conn.cursor()

cur.execute("""
            INSERT INTO global_crypto_data (ticker,open_time,open,high,low,close,coin_volume,quote_asset_volume,total_trades,market_buy_volume,market_buy_quote_volume,delta,close_Time)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s.%s)
            for 
            (all_data[])
            """)

conn.commit()
cur.close()
conn.close()







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
