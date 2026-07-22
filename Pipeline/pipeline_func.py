import requests
import json
import time
from datetime import datetime, timezone
# from dataclasses import dataclass

def transform_24h_ticker(raw):
    return {
        'ticker': raw['symbol'],
        'open_time': convert_raw_time(raw['openTime']),
        'price_change': float(raw['priceChange']),
        'price_change_percent': float(raw['priceChangePercent']),
        'vwap': float(raw['weightedAvgPrice']),
        'volume': float(raw['volume']),
        'quote_volume': float(raw['quoteVolume']),
        'close_time': convert_raw_time(raw['closeTime'])
    }

def fetch_24h_tickers():
    url = 'https://api.binance.com/api/v3/ticker/24hr'

    transformed_price_chg = []
    transformed_vol_chg = []
    price_chg_300coin_ticker = None
    volume_chg_300coin_ticker = None
    
    max_count = 3
    start_count = 0

    while start_count < max_count:
    
        try:
            response = requests.get(url)

            if response.status_code == 200:
            
                usdt_assets = [coin_data for coin_data in response.json() 
                                    if coin_data['symbol'].endswith('USDT')]
                
                price_chg_300coin = sorted( usdt_assets, key=lambda x: float(x['priceChangePercent']), reverse=True)[:300]
                volume_chg_300coin = sorted( usdt_assets, key=lambda x: float(x['quoteVolume']), reverse=True)[:300]

                price_chg_300coin_ticker = [ticker['symbol'] for ticker in price_chg_300coin]
                volume_chg_300coin_ticker = [ticker['symbol'] for ticker in volume_chg_300coin]

                for data in price_chg_300coin:
                    transformed_price_chg.append(transform_24h_ticker(data))
                
                for data in volume_chg_300coin:
                    transformed_vol_chg.append(transform_24h_ticker(data))
                break

            elif response.status_code == 429:
                retry_time = int(response.headers.get('Retry-After', 30))
                print('429 error, slowing down calls')
                time.sleep(retry_time)
                start_count += 1
                continue

            elif response.status_code == 418:
                print('now youve done it')
                break
        
        except Exception as error:
            print(error)
            return None, None, None, None
    
    return price_chg_300coin_ticker,volume_chg_300coin_ticker,transformed_price_chg,transformed_vol_chg

def convert_raw_time(raw_time):
    return datetime.fromtimestamp(raw_time/1000 , tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S") 

def convert_standard_time(year, month, day, hour, minute, second):
    dt = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc) 
    return int(dt.timestamp() * 1000)

def transform_kline(raw,coin):
    return {'ticker' : coin,
            'open_time' : convert_raw_time(raw[0]),
            'open' : float(raw[1]),
            'high' : float(raw[2]),
            'low' : float(raw[3]),
            'close' : float(raw[4]),
            'coin_volume' : float(raw[5]),
            'quote_asset_volume' : float(raw[7]),
            'total_trades' : int(raw[8]),
            'market_buy_volume' : float(raw[9]),
            'market_buy_quote_volume' : float(raw[10]),
            'close_time' : convert_raw_time(raw[6])
            }

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
                    'interval': '1d',
                    'limit': 500,
                    'startTime' : convert_standard_time(2026,6,1,0,0,0),
                    'endTime' : convert_standard_time(2026,6,30,0,0,0) 
                }

                response = requests.get(url, params=params)

                if response.status_code == 200:
                    print("API working")
                    for raw in response.json():
                        all_data.append(transform_kline(raw,coin))        
                    
                    check_limit = response.headers.get('x-mbx-used-weight-1m')
                    if int(check_limit) > 5400:
                        print("90 percent limit reached, API calls slowing down")
                        time.sleep(4)
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

