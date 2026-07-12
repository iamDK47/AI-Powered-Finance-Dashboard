import requests
import json
import time

def twenty_coins(coins):

    All_data =[]

    for coin in coins:
        Exec_count = 0
        Exec_limit = 3
        while Exec_count < Exec_limit:
            try:    
                response = requests.get(f"https://api.binance.com/api/v3/klines?symbol={coin}&interval=1m&limit=1")

                if response.status_code == 200:
                    print("API working")
                    All_data.append({'ticker' : coin , 'data' : response.json()[0]})    
                    with open('response.json', 'w') as f:
                        json.dump([All_data,dict(response.headers)],f,indent =2)
                    check_limit = response.headers.get('x-mbx-used-weight-1m')
                    if int(check_limit) > 5000:
                        time.sleep(2)
                    break

                elif response.status_code == 429:
                    retry_time = int(response.headers.get('Retry-After',30))
                    print("STOPPP, TOO MANY REQUESTS")
                    time.sleep(retry_time)
                    Exec_count += 1
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

    return All_data