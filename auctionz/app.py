import falcon

from auctionz.view.auction import BidGet, BidAdd
from auctionz.util.constants import AUCTION


app = falcon.App()

get_bid = BidGet()
add_bid = BidAdd()

app.add_route(AUCTION + '/{item}', get_bid)
app.add_route(AUCTION + '/add-bid', add_bid)
