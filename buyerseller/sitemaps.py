from .models import *
from django.contrib.sitemaps import Sitemap


class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Product.objects.filter(status=1)


