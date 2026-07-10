from kafka import KafkaConsumer
import json

consumer = KafkaConsumer( #Connects to the Kafka broker and listens for messages.
    "order-created", #The topic this consumer subscribes to.
    bootstrap_servers="kafka:9092", #The address of the Kafka broker.
    auto_offset_reset="earliest",#If the consumer starts for the first time, it begins reading from the oldest available message.
    group_id="email-group",#This consumer belongs to the email-group.
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))#Converts the JSON message back into a Python dictionary.
)

print("Email Consumer Started...")

for message in consumer:
    order = message.value

    print(f"Sending email for Order ID: {order['order_id']} to User ID: {order['user_id']}")