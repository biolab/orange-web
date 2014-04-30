"""Here we define custom django tags"""
from django import template
import feedparser

register = template.Library()


@register.inclusion_tag('feed_results.html')
def grab_feed():
    """Grabs an RSS/Atom feed. Django will cache the content."""
    feed = feedparser.parse('http://orange.biolab.si/blog/rss/')
    if not feed.bozo:
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
                }
    else:
        raise feed.bozo_exception
