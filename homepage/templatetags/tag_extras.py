"""Here we define custom django tags"""
import logging
from io import BytesIO
from os import path

from datetime import datetime as dt

import re
from django import template
from django.core.urlresolvers import reverse
from docutils.core import publish_parts
from django.conf import settings

import feedparser
import requests
# noinspection PyUnresolvedReferences
from six.moves import xmlrpc_client as xmlrpclib

logger = logging.getLogger(__name__)
register = template.Library()

post_max_length = 450  # max length of post excerpt lengt
post_with_image_length = 180  # length of post that contains image


def grab_feed_all():
    """Grabs an RSS/Atom feed. Django will cache the content."""
    rss_feed = 'https://blog.biolab.si/feed/'
    try:
      resp = requests.get(rss_feed, timeout=3.0)
    except requests.ReadTimeout:
      logger.warn("Timeout when reading RSS %s", rss_feed)
      return
    except requests.exceptions.ConnectionError:
      # This problem may be caused by bad DNS server
      logger.warn("Connection error when reading RSS %s", rss_feed)
      return

    # Put it to memory stream object universal feedparser
    content = BytesIO(resp.content)

    # Parse content
    feed = feedparser.parse(content)
    if feed.bozo == 0:
        # Parses first 3 entries from remote blog feed.
        entries = []
        for i in range(3):
            pub_date = feed['entries'][i]['published'][:-6]
            df = '%a, %d %b %Y %H:%M:%S'
            description = feed['entries'][i]['description']
            image = None
            # take image from description if exist
            if '<img' in description:
                image_from, image_to = description.index('<img'), description.index('/>')
                image = description[image_from:image_to+2]
                description = description[image_to + 2:]
                image = image[image.index('src') + 5:]
                image = image[:image.index('"')]
            # shorten a description
            description = cut_string(
                description.replace("&#160;", "").replace("[&#8230;]", ""),
                post_length=post_max_length if image is None else post_with_image_length)
            entry = {
                'title': feed['entries'][i]['title'],
                'link': feed['entries'][i]['link'],
                'description': description,
                'published': dt.strptime(pub_date, df).strftime('%d %b'),
                'image': image
            }
            entries.append(entry)
        return {'entries': entries,
                'bozo': False
                }
    else:
        return {'bozo': True}


def cut_string(string, post_length):
    if len(string) < post_length:
        return string
    else:
        # find fist space before limit
        for i in range(post_length, 0, -1):
            if string[i] == ' ':
                break
        return string[:i]


@register.inclusion_tag('feed_results.html')
def blog_feed_small():
    return grab_feed_all()


@register.inclusion_tag('feed_bar.html')
def blog_feed_bar():
    return grab_feed_all()


@register.inclusion_tag('toolbox_widgets.html')
def toolbox_widgets(widget_js):
    return {'toolbox': widget_js}


@register.inclusion_tag('testimonials.html')
def testimonials_tag(data):
    return {'testimonials': data}
