import json

from kafka import KafkaConsumer, KafkaProducer
from redis import Redis

from auctionz.util.constants import AUCTION_BID

kafka_producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

kafka_consumer = KafkaConsumer(
    AUCTION_BID,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

redis = Redis(host="localhost", port=6379, db=0)
