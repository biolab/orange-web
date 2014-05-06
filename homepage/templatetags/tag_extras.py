"""Here we define custom django tags"""
from django import template
import feedparser

from django.conf import settings

register = template.Library()


@register.inclusion_tag('feed_results.html')
def grab_feed_all():
    """Grabs an RSS/Atom feed. Django will cache the content."""
    feed = feedparser.parse('http://' + settings.ALLOWED_HOSTS[0] + '/blog/rss/')
    if feed.bozo == 0:
        # Parses first 6 entries from remote blog feed.
        entries_1 = []
        entries_2 = []
        for i in range(6):
            entry = {
                'title': feed['entries'][i]['title'],
                'link': feed['entries'][i]['link'],
                'text': feed['entries'][i]['summary_detail']['value']
            }
            if i % 2 == 0:
                entries_1.append(entry)
            else:
                entries_2.append(entry)
        return {'entries_1': entries_1,
                'entries_2': entries_2,
                'bozo': False
                }
    else:
        return {'bozo': True}


@register.inclusion_tag('first_feed_result.html')
def grab_feed_first():
    """Grabs an RSS/Atom feed. Django will cache the content."""
    feed = feedparser.parse('http://' + settings.ALLOWED_HOSTS[0] + '/blog/rss/')
    if feed.bozo == 0:
        # Parses first entry from remote blog feed.
        return {'title': feed['entries'][0]['title'],
                'link': feed['entries'][0]['link'],
                'text': feed['entries'][0]['summary_detail']['value'],
                'bozo': False
                }
    else:
        return {'bozo': True}
