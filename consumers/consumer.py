import json
from confluent_kafka import Consumer

consumer = Consumer({
  'bootstrap.servers': 'localhost:9092',
  'group.id': 'flight-group',
  'auto.offset.reset': 'earliest'
})

consumer.subscribe(['flight-telemetry'])

print("Listening for messages...")

try:
  while True:
    msg = consumer.poll(1.0)
    if msg is None:
      continue
    if msg.error():
      print(f"Error: {msg.error()}")
      continue
    flight = json.loads(msg.value().decode('utf-8'))
    print(f"flight: {flight}")

except KeyboardInterrupt:
  pass
finally:
  consumer.close()