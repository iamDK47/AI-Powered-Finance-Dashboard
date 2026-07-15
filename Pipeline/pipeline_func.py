import requests
import json
import time
from datetime import datetime
# from dataclasses import dataclass


def transform_kline(raw,coin):
    return {'ticker' : coin,
            'open_time' : convert_time(raw[0]),
            'open' : float(raw[1]),
            'high' : float(raw[2]),
            'low' : float(raw[3]),
            'close' : float(raw[4]),
            'coin_volume' : float(raw[5]),
            'quote_asset_volume' : float(raw[7]),
            'total_trades' : int(raw[8]),
            'market_buy_volume' : float(raw[9]),
            'market_buy_quote_volume' : float(raw[10]),
            'close_time' : convert_time(raw[6])
            }

def convert_time(raw_time):
    return datetime.fromtimestamp(raw_time/1000).strftime("%Y-%m-%d %H:%M:%S") 

def fetch_klines(coins):

    all_data =[]

    for coin in coins:
        exec_count = 0
        max_retries = 3
        while exec_count < max_retries:
            try:    

                url = "https://api.binance.com/api/v3/klines"
                params = {
                    'symbol': coin,
                    'interval': '1m',
                    'limit': 1
                }

                response = requests.get(url, params=params)

                if response.status_code == 200:
                    print("API working")
                    raw = response.json()[0]
                    all_data.append(transform_kline(raw,coin))        
                    
                    check_limit = response.headers.get('x-mbx-used-weight-1m')
                    if int(check_limit) > 5400:
                        print("90 percent limit reached, API calls slowing down")
                        time.sleep(2)
                    break

                elif response.status_code == 429:
                    retry_time = int(response.headers.get('Retry-After',30))
                    print("STOPPP, TOO MANY REQUESTS")
                    time.sleep(retry_time)
                    exec_count += 1
                    continue

                elif response.status_code == 418:
                    print("NOW YOU'VE DONE IT")
                    break

                else:
                    print("failed to connect")
                    print(response.text)
                    break

            except Exception as error:
                print(f"{error}")
                exec_count += 1
                continue

    with open('response.json', 'w') as f:
        json.dump(all_data,f,indent =2)
        
    return all_data