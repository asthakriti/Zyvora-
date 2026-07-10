from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "order-created",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="earliest",
    group_id="analytics-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Analytics Consumer Started...")

for message in consumer:
    order = message.value

    print(f"Updating analytics for Order {order['order_id']}")