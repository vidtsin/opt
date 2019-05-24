from ..base import ShopifyResource
from ..mixins import Metafields
from ..mixins import Events
from transaction import Transaction


class Order(ShopifyResource, Metafields, Events):

    def close(self):
        self._load_attributes_from_response(self.post("close"))

    def open(self):
        self._load_attributes_from_response(self.post("open"))

    def cancel(self, **kwargs):
        self._load_attributes_from_response(self.post("cancel", **kwargs))

    def transactions(self):
        return Transaction.find(order_id=self.id)

    def capture(self, amount=""):
        return Transaction.create({"amount": amount, "kind": "capture", "order_id": self.id})
