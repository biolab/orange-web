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


# TODO: CSS na homepage, da se fork ikona ne rotira
# TODO: download_choices(), da bo class DownloadLink zrenderiral link string direktno, odvisno od platforme, bitnosti, verzije ...
# TODO: Zaznavanje 64-bit sistema pri USER_AGENT_STRING
@register.inclusion_tag('download_link.html')
def download_choices(os, pure=False, ver=None):
    """
    os has to be set to either 'win' or 'mac' in template.
    ver has to be either '2.5', '2.6, or '2.7'.
    """
    wanted_files = []
    ffi = open(settings.DOWNLOAD_SET_PATTERN % os, 'rt')
    for line in ffi:
        ep = line.find('=')
        key = line[:ep].strip()
        value = line[ep+1:].strip()
        if value:
            if os == 'win':
                if pure:
                    pykey = '%s_PY%s' % (key, ver)
                    wanted_files.append(pykey)
            else:
                # if os == 'mac'
                wanted_files.append(key)
    ffi.close()


class DownloadLink(template.Node):
    def __init__(self, download_link):
        self.download_link = download_link

    def render(self, context):
        return self.download_link