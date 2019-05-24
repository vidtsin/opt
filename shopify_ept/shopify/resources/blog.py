from ..base import ShopifyResource
from ..mixins import Metafields
from ..mixins import Events
from article import Article


class Blog(ShopifyResource, Metafields, Events):

    def articles(self):
        return Article.find(blog_id=self.id)
