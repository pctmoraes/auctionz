import json

from kafka import KafkaProducer
from redis import Redis


kafka_producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

redis = Redis(host="localhost", port=6379, db=0)

