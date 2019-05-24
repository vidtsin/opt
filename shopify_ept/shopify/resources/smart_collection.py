from ..base import ShopifyResource
from ..mixins import Metafields
from ..mixins import Events
import product


class SmartCollection(ShopifyResource, Metafields, Events):

    def products(self):
        return product.Product.find(collection_id=self.id)
