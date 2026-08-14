from database.postgres_conn import postgres_conn

import numpy as np
import pandas as pd
import json

def db_data():

    conn = postgres_conn()
    with conn.cursor() as curr:

        query = """SELECT close_time,close, quote_asset_volume,open_time,ticker 
                   FROM global_crypto_data
                   WHERE open_time BETWEEN '2026-06-01 00:00:00.000' AND '2026-06-30 00:00:00.000' 
                   ORDER BY quote_asset_volume DESC, ticker DESC"""
        
                #    AND ticker in (SELECT DISTINCT ticker FROM global_crypto_data)
        # curr.execute(query)
        # data = curr.fetchall()

        data = pd.read_sql(query, conn)

        # df = pd.DataFrame(data)

        print(data)
        # print(df)

    conn.commit()
    conn.close()

db_data()