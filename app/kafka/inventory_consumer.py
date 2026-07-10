from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "order-created",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="earliest",
    group_id="inventory-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Inventory Consumer Started...")

for message in consumer:
    order = message.value

    print(f"Reducing inventory for Order {order['order_id']}")