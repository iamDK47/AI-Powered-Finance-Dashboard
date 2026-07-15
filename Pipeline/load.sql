INSERT INTO global_crypto_data (ticker,open_time,open,high,low,close,coin_volume,quote_asset_volume,total_trades,market_buy_volume,market_buy_quote_volume,delta,close_Time)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s.%s)
            for 
            (all_data[])