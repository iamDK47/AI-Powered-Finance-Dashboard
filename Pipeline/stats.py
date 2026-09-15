from database.postgres_conn import postgres_conn

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import dtale

# def edit_pg():
#     conn = postgres_conn()
#     with conn.cursor() as curr:
#         query = """TRUNCATE TABLE global_crypto_data RESTART IDENTITY"""
#         # query = """DROP TABLE global_crypto_data"""

#         curr.execute(query)
#     conn.commit()
#     conn.close()

# edit_pg()

def db_data():

    conn = postgres_conn()
    # with conn.cursor() as curr:

    query = """SELECT close_time,close, quote_asset_volume,open_time,ticker
                FROM global_crypto_data
                WHERE open_time BETWEEN '2026-06-01 00:00:00.000' AND '2026-06-30 00:00:00.000'"""

    
    # curr.execute(query)
    # data = curr.fetchall()

    data = pd.read_sql(query,conn)
    # print(data)

    conn.commit()
    conn.close()

    data_pivot = data.pivot(index = 'open_time' , columns='ticker', values='close')
    # print(data_pivot)

    # returns = data_pivot.drop(columns='BTCUSDT').pct_change() * 100
    returns = data_pivot.pct_change() * 100
    # print(returns)

    # btc_pct = data_pivot['BTCUSDT'].pct_change() * 100
    # print(btc_pct)
    # corr = returns.corrwith(btc_pct)
    corr = returns.rolling(29).corr(returns['BTCUSDT'])
    # print(corr)
    corrm = returns.corr()
    print(corrm)
    btccc = corrm.loc['ETHUSDT','BTCUSDT']
    print(btccc)

    btcc = corr.loc[:, 'ETHUSDT']
    print(btcc)

    # df_corr = pd.DataFrame(corr)
    # df_corrm = pd.DataFrame(corrm)
    # dtale.show(df_corr, port=8080, open_browser=True)
    # dtale.show(df_corrm, port=8080, open_browser=True)
    # high_corr = corr[corr >= 0.80]
    # print(high_corr)

    # input('press enter')

db_data()
