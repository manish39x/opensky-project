from ingestion.config import Config
from ingestion.auth.token_manager import TokenManager
from ingestion.opensky_service import OpenSkyFlightService, OpenSkyFetchError
from ingestion.kafka_producer import KafkaProducerService
from logging import getLogger
import time

logger = getLogger(__name__)

config = Config()
token_manager = TokenManager(config.opensky_client_id,
                             config.opensky_client_secret.get_secret_value(), config.proxy_url)
opensky_flight = OpenSkyFlightService(config, token_manager)

kafka_producer = KafkaProducerService(config)

try:
  while True:
    try:
      result = opensky_flight.fetch_states()
      fetch_time = result['time']
      states = result['states']
      for state in states:
        kafka_producer.publish(state, fetch_time)
    except OpenSkyFetchError as e:
      logger.error(f"Opensky data fetch failed {e}. retrying next cycle")
    except Exception as e:
      logger.error(f"Unexpected loop in ingestion loop")
    time.sleep(config.poll_interval_seconds)
except KeyboardInterrupt:
  logger.info("Shutdown signal received. Exiting data producer...")
finally:
  logger.info("Flushing Remaing Kafka messages")
  kafka_producer.flush()

