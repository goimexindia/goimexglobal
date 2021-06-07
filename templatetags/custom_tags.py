from django import template

register = template.Library()


@register.inclusion_tag("buyerseller\ecomerce.html")
def gt(a, b):
    return a > 1
