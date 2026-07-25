import time
import json
from confluent_kafka import Producer
from generator.fetch_flight_telemetry import get_flight_telemetry

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

def delivery_report(err, msg):
  if err:
    print(f"Failed: {err}")
  else:
    print(f"Sent to partition {msg.partition()} offset {msg.offset()}")


while True:
  flights_data = get_flight_telemetry()
  flights = flights_data.get("states", [])
  for flight in flights:
    payload = {
      "time": flights_data.get("time"),
      "flight_vector": flight
    }
    icao24_key = str(flight[0]).encode('utf-8') if flight else None
    producer.produce(
      topic="flight-telemetry",
      value=json.dumps(payload),
      key=icao24_key,
      callback=delivery_report
    )
    producer.poll(0)
  time.sleep(10)