import json
from confluent_kafka import Consumer

consumer = Consumer({
  'bootstrap.servers': 'localhost:9092',
  'group.id': 'taxi-group',
  'auto.offset.reset': 'earliest'
})

consumer.subscribe(['taxi-trips'])

print("Listening for messages...")

try:
  while True:
    msg = consumer.poll(1.0)
    if msg is None:
      continue
    if msg.error():
      print(f"Error: {msg.error()}")
      continue
    trip = json.loads(msg.value().decode('utf-8'))
    print(f"[P{msg.partition()} | offset {msg.offset()}] "
          f"{trip['trip_id']} | {trip['user_id']} | ${trip['fare_per_person']} | loc: {trip['pickup_location']}")

except KeyboardInterrupt:
  pass
finally:
  consumer.close()