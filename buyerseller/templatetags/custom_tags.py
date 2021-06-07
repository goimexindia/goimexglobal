from django import template

register = template.Library()


@register.filter(name='gt')
def gt(a, b):
    return a > 1
