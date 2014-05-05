"""Start of orange-web app"""
from django import template

register = template.Library()


def cache_feed(value):
    """RSS feed caching"""
    return value


register.filter('cache_feed', cache_feed, is_safe=True)
