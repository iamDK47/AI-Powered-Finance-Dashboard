import requests
import os

beta_API = {'bitcoin' : {'usd' : 69420.96}}
Mock_API = True

coins = ['bitcoin,ethereum,solana,cardano,ripple']
result = ','.join(coins)
The_url = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids={result}"

custom_header = {
 "x-cg-demo-api-key": os.getenv('API_KEY')
}

try:

  if Mock_API:
    mock_result = beta_API['bitcoin']['usd']
    print(f"BETA API WORKING price is ${mock_result:,}")

  else:
    response = requests.get(The_url, headers=custom_header)

    if response.status_code == 200:
      print("api is working")
      response_json = response.json()
      print(response_json)

    else:  
      print("failed to connect")
      print(response.text)

except Exception as err:
  print(f"error caught: {err}")