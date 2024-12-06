import logging
import json

import falcon

from auctionz.container.config import kafka_consumer, kafka_producer, redis
from auctionz.util.constants import AUCTION_BID


class BidGet:
    def on_get(self, req, resp, item):
        response = {}

        try:
            if bid := float(redis.get(item)):
                for message in kafka_consumer:
                    if message.key == item:
                        if float(message.value) > float(bid):
                            bid = float(message.value)

                redis.set(item, bid)
                response['message'] = f'The bid for item {item} is ${bid}'
                resp.text = json.dumps(response, ensure_ascii=False)
            else:
                response['message'] = f'No bid found for item {item}'
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}

class BidAdd:
    def on_post(self, req, resp):
        try:
            item = req.get_param('item')
            bid = req.get_param('bid')

            if not item or not bid:
                raise falcon.HTTPBadRequest(
                    "Missing Parameters",
                    "Both 'item' and 'bid' must be provided.",
                )

            message = {
                'item': item,
                'bid': bid
            }

            kafka_producer.send(
                topic=AUCTION_BID,
                key=item.encode('utf-8'),
                value=message
            )

            resp.status = falcon.HTTP_201
            resp.text = json.dumps(
                {
                    'status': 'success',
                    'message': f'Was sent to Kafka bid: {bid} for {item}'
                }, 
                ensure_ascii=False
            )
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}
