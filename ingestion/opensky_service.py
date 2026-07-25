import requests
import logging
import time
from ingestion.config import Config
from ingestion.auth.token_manager import TokenManager

logger = logging.getLogger(__name__)

class OpenSkyFetchError(Exception):
  pass

class OpenSkyFlightService:
  def __init__(self, config:Config, token_manager:TokenManager):
    self.config = config
    self.token_manager = token_manager

  def _request(self) -> requests.Response:
    url = f"{self.config.opensky_base_url}/api/states/all"
    params = {
      "lamin":self.config.bbox.lamin,
      "lomin":self.config.bbox.lomin,
      "lamax":self.config.bbox.lamax,
      "lomax":self.config.bbox.lomax
    }
    try:
        logger.debug(f"Initialting request to {url} with params {params}")
        response = requests.get(
          url=url,
          timeout=self.config.request_timeout_seconds,
          headers=self.token_manager.headers(),
          params=params,
          proxies = {
                      'http': self.config.proxy_url,
                      'https': self.config.proxy_url
                    }
        )
        return response
    except Exception as e:
      logger.exception("Telemetry Fetch Crash: Connection or timeout error occurred.")
      raise OpenSkyFetchError(e)

  def _request_with_retry(self):
    backoff_delay = self.config.base_backoff_seconds

    for attempt in range(self.config.max_retries):
      response = self._request()

      if response.status_code==200:
        logger.info(f"Successfully fetched aircraft telemetry on attempt {attempt + 1}")
        return response.json()
      
      elif response.status_code==429:
        retry_after = response.headers.get("Retry-After")
        if retry_after and retry_after.isdigit():
          wait_time = int(retry_after)
        else:
          wait_time = backoff_delay
          backoff_delay *= 2
        logger.warning(
            f"Rate limited (429). Retrying in {wait_time}s... "
            f"Attempt {attempt + 1}/{self.config.max_retries}"
        )
        time.sleep(wait_time)

      else:
        logger.error(f"Server responded with unhandled status code: {response.status_code}")
        time.sleep(backoff_delay)

    raise OpenSkyFetchError(f"Failed to fetch data after {self.config.max_retries} attempts.")
        

  def fetch_states(self):
    data = self._request_with_retry()

    if not data or 'states' not in data or data['states'] is None:
      logger.info("Opensky payload empty or no flight in the boundBox")
      return []

    logger.info(f"Retrieved {len(data['states'])} active aircraft states.")
    return data.get("states", [])