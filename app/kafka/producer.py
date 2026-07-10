from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",   # Docker service name
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def publish_order_created(order_id: int, user_id: int):
    future = producer.send(
        "order-created",
        {
            "order_id": order_id,
            "user_id": user_id
        }
    )

    metadata = future.get(timeout=10)

    print(f"Sent to Partition: {metadata.partition}")
    producer.flush()