import requests


API_URI = "https://opensky-network.org"
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
proxies = {
  "http": "socks5h://127.0.0.1:1080",
  "https": "socks5h://127.0.0.1:1080"
}

try:
  res = requests.get(
    url=f"{API_URI}/api/states/all",
    proxies=proxies,
    headers=headers,
    timeout=45 
  )
  if res.status_code == 200:
    print("Success")
    data = res.json()

    print(data)
except Exception as e:
  print(e)