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

        # curr.execute(query)
        # data = curr.fetchall()

        data = pd.read_sql(query, conn)

        data_pivot = data.pivot(index = 'open_time' , columns='ticker', values='close')

        # log_return = np.log(data_pivot / data_pivot.shift(1))

        # sum = log_return['BTCUSDT'].sum()
        # print(sum)

        # df = pd.DataFrame(data)

        # print(data)
        print(data_pivot)
        # print(log_return)
        # print(log_return['BTCUSDT'])
        # print(df)

    conn.commit()
    conn.close()

db_data()
