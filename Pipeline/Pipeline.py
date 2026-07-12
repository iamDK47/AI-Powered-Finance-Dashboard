import psycopg2 
import os
from dotenv import load_dotenv
import datetime from datetime
load_dotenv()
from pipelineExc import twenty_coins

coins = ['BTCUSDT','ETHUSDT','BNBUSDT','XRPUSDT','SOLUSDT','TRXUSDT','DOGEUSDT','XLMUSDT','ZECUSDT','ADAUSDT','LINKUSDT','GRAMUSDT','DEXEUSDT','LTCUSDT','HBARUSDT','UNIUSDT','SUIUSDT','AVAXUSDT','SHIBUSDT','NEARUSDT']

All_data = twenty_coins

load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    dbname="Crypto_Analytics",
    user="postgres",
    password= os.getenv("DB_Password"),
    port=5432
)

cur = conn.cursor()

cur.execute("""
            INSERT INTO global_crypto_data()
            """)

conn.commit()
cur.close()
conn.close()

















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
