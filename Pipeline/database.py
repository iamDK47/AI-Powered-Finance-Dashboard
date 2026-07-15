#cd pipeline , \venv\Scripts\Activate
import psycopg2 
import os
from dotenv import load_dotenv
load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    dbname="Crypto_Analytics",
    user="postgres",
    password = os.getenv("DB_Password"),
    port=5432
)

def load_data(all_data):

    cur = conn.cursor()

    for data in all_data:
        delta = data["market_buy_volume"] - (data["coin_volume"] - data["market_buy_volume"])
        cur.execute("""
            INSERT INTO global_crypto_data (ticker,open_time,open,high,low,close,coin_volume,quote_asset_volume,total_trades,market_buy_volume,market_buy_quote_volume,delta,close_time)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (data["ticker"],data["open_time"],data["open"],data["high"],data["low"],data["close"],data["coin_volume"],data["quote_asset_volume"],data["total_trades"],data["market_buy_volume"],data["market_buy_quote_volume"],delta,data["close_time"])
        )
    conn.commit()
    cur.close()
    conn.close()
