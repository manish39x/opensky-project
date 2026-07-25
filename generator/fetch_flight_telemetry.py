import requests 
from dotenv import load_dotenv
from ingestion.auth.token_manager import TokenManager

load_dotenv()

BOUND_BOX = [43.0, -5.0, 55.0, 16.0]

OPENSKY_API_URI = "https://opensky-network.org"
proxies = {
    'http': 'socks5h://127.0.0.1:1080',
    'https': 'socks5h://127.0.0.1:1080'
}
token = TokenManager()

def get_flight_telemetry():
  try:
    print("Fetching Opensky data...")
    response = requests.get(
      f"{OPENSKY_API_URI}/api/states/all",
      timeout=45,
      headers=token.headers,
      proxies=proxies
    )
    if response.status_code == 200:
      flight_data = response.json()
      total_flights = len(flight_data.get("states", []))
      print(f"🎉 Success! Retrieved {total_flights} global flights through the proxy.")
      return flight_data
    else:
      print(f"Error {response.status_code}: {response.text}")
      return []
  except Exception as e:
    print(f"Telemetry Fetch Crash: {e}")
    raise e