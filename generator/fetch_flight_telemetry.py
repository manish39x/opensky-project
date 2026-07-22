import os
import requests 
from dotenv import load_dotenv

load_dotenv()

OPENSKY_API_URI = "https://opensky-network.org"
proxies = {
    'http': 'socks5h://127.0.0.1:1080',
    'https': 'socks5h://127.0.0.1:1080'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
  print("Fetching Opensky data...")
  response = requests.get(
    f"{OPENSKY_API_URI}/api/states/all",
    timeout=45,
    headers=headers,
    proxies=proxies
  )
  if response.status_code == 200:
    flight_data = response.json()
    total_flights = len(flight_data.get("states", []))
    print(f"🎉 Success! Retrieved {total_flights} global flights through the proxy.")
    print(flight_data.get("states", [])[0])
  else:
    print(f"Error {response.status_code}: {response.text}")
except Exception as e:
  print(f"Telemetry Fetch Crash: {e}")
  raise e