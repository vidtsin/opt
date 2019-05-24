from ..base import ShopifyResource
from ..mixins import Metafields
from ..mixins import Events


class Page(ShopifyResource, Metafields, Events):
    pass
