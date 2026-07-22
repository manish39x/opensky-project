import json
import time
import random
from datetime import datetime
from confluent_kafka import Producer
from faker import Faker

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

def delivery_report(err, msg):
  if err:
    print(f"Failed: {err}")
  else:
    print(f"Sent to partition {msg.partition()} offset {msg.offset()}")


fake = Faker()

def generate_trip_event():
  return {
    "trip_id": fake.uuid4(),
    "user_id": fake.random_int(min=1000, max=9999),
    "passenger_count": fake.random_int(min=1, max=4),
    "fare_per_person": round(random.uniform(15.0, 120.0), 2),
    "trip_start_timestamp": datetime.utcnow().isoformat,
    "pickup_location": random.choice(["Manhattan", "Texas", "Berlin"])
  }


while True:
  trip = generate_trip_event()
  producer.produce(
    topic="taxi-trips",
    key=trip["trip_id"],
    value=json.dumps(trip),
    callback=delivery_report
  )
  producer.poll(0)
  time.sleep(2)