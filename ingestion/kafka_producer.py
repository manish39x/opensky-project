from ingestion.config import Config
from logging import getLogger
from confluent_kafka import Producer
import json

logger = getLogger(__name__)



## KAFKA PRODUCER SERVICE LOGIC
class KafkaProducerService:
  def __init__(self, config: Config):
    self.config = config
    conf = {'bootstrap.servers': self.config.kafka_bootstrap_servers}
    self.producer = Producer(conf)

  def publish(self, record: list, time: int) -> None:
    icao24  = str(record[0]).encode('utf-8') if record and record[0] else None 
    if not icao24:
      return 

    payload = {
      "time": time,
      "flight_vector": record
    }
    data = json.dumps(payload)
    self.producer.produce(
      topic=self.config.kafka_topic,
      value=data,
      key=icao24,
      callback=self._delivery_report
    )
    self.producer.poll(0)

  def flush(self, timeout:float = 10.0) -> int:
    res = self.producer.flush(timeout)
    return res
    

  def _delivery_report(self, err, msg) -> None:
    if err:
      logger.error(f"kafka error: {err}")
    else:
      logger.debug(f"Sent to partition {msg.partition()} offset {msg.offset()}")

