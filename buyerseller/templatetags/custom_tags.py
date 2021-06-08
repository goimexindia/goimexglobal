from django import template

from accounts.models import Profile
from blog.models import Post
from buyerseller.models import Product

register = template.Library()


@register.filter(name='gt')
def gt(a, b):
    return a > 1


@register.inclusion_tag("latest.html")
def show_latest_name(total=5):
    last = Product.objects.order_by('-id')[:total]
    return {'last': last}


@register.inclusion_tag("latestpost.html")
def show_latest_post(total=5):
    last = Post.objects.order_by('-id')[:total]
    return {'last': last}


@register.inclusion_tag("latestcompany.html")
def show_latest_company(total=5):
    last = Profile.objects.exclude(organization__isnull=True).order_by('-id')[:total]
    return {'last': last}


@register.inclusion_tag("latestproduct.html")
def show_latest_product(total=8):
    last = Product.objects.order_by('-id')[:total]
    return {'last': last}
