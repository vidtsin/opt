from ..base import ShopifyResource
from ..mixins import Metafields
from ..mixins import Events
from collect import Collect
import product


class CustomCollection(ShopifyResource, Metafields, Events):

    def products(self):
        return product.Product.find(collection_id=self.id)

    def add_product(self, product):
        return Collect.create({'collection_id': self.id, 'product_id': product.id})

    def remove_product(self, product):
        collect = Collect.find_first(collection_id=self.id, product_id=product.id)
        if collect:
            collect.destroy()
