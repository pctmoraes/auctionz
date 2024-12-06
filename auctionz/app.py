import falcon

from auctionz.util.constants import AUCTION
from auctionz.view.auction import BidAdd, BidGet

app = falcon.App()

get_bid = BidGet()
add_bid = BidAdd()

app.add_route(AUCTION + '/{item}', get_bid)
app.add_route(AUCTION + '/add', add_bid)
