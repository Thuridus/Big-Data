import time
from essential_generators import DocumentGenerator
from kafka import KafkaProducer

gen = DocumentGenerator()

producer = KafkaProducer(
    bootstrap_servers='my-cluster-kafka-bootstrap:9092')

while True:
    next_msg = gen.sentence()
    print(f"Sending message: {next_msg}")
    future = producer.send("big_data_demo", next_msg.encode())
    result = future.get(timeout=5)
    print(f"Result: {result}")
    time.sleep(2)