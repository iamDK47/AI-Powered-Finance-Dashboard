from psycopg2.extras import execute_values
from database.postgres_conn import postgres_conn

def load_kline(all_data, commit_every=50_000, batch_size=5000):
    conn = postgres_conn()
    insert_sql = """
        INSERT INTO global_crypto_data
        (ticker,open_time,open,high,low,close,coin_volume,quote_asset_volume,
         total_trades,market_buy_volume,market_buy_quote_volume,delta,close_time)
        VALUES %s
    """

    with conn.cursor() as cur:
        rows = []
        for i, data in enumerate(all_data, start=1):
            delta = data["market_buy_volume"] - (data["coin_volume"] - data["market_buy_volume"])
            rows.append((
                data["ticker"], data["open_time"], data["open"], data["high"], data["low"],
                data["close"], data["coin_volume"], data["quote_asset_volume"],
                data["total_trades"], data["market_buy_volume"], data["market_buy_quote_volume"],
                delta, data["close_time"]
            ))

            if i % commit_every == 0:
                execute_values(cur, insert_sql, rows, page_size=batch_size)
                conn.commit()
                rows = [] 

        if rows: 
            execute_values(cur, insert_sql, rows, page_size=batch_size)
            conn.commit()

    conn.close()

def load_corr_cov(by_price_chg):
    conn = postgres_conn()
    with conn.cursor() as curr:

        for data in by_price_chg:
            curr.execute("""
                INSERT INTO corr_cov (ticker, open_time, price_change, price_change_percent, vwap, volume, quote_volume, close_time)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (data['ticker'],data['open_time'],data['price_change'],data['price_change_percent'],data['vwap'],data['volume'],data['quote_volume'],data['close_time'])
            )
    conn.commit()
    conn.close()