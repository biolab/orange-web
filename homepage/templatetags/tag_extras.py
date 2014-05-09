"""Here we define custom django tags"""
from django import template
import feedparser
import re

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


def download_choices(os):
    if os == 'win':
        downloads = {
            'winw25': None,
            'winw26': None,
            'winw27': None,
            'win25': None,
            'win26': None,
            'win27': None,
            'bio26': None,
            'bio27': None,
            'text26': None,
            'text27': None,
            'source': None,
        }
        ffi = open(settings.DOWNLOAD_SET_PATTERN % os, 'rt')
        for line in ffi:
            ep = line.find('=')
            key = line[:ep].strip()
            value = line[ep+1:].strip()
            if key == 'WIN_SNAPSHOT':
                downloads['win25'] = '%s-py2.5.exe' % value
                downloads['win26'] = '%s-py2.6.exe' % value
                downloads['win27'] = '%s-py2.7.exe' % value
            elif key == 'WIN_PYTHON_SNAPSHOT':
                downloads['winw25'] = '%s-py2.5.exe' % value
                downloads['winw26'] = '%s-py2.6.exe' % value
                downloads['winw27'] = '%s-py2.7.exe' % value
            elif key == 'ADDON_BIOINFORMATICS_SNAPSHOT':
                downloads['bio26'] = '%s-py2.6.exe' % value
                downloads['bio27'] = '%s-py2.7.exe' % value
            elif key == 'ADDON_TEXT_SNAPSHOT':
                downloads['text26'] = '%s-py2.6.exe' % value
                downloads['text27'] = '%s-py2.7.exe' % value
            elif key == 'SOURCE_SNAPSHOT':
                downloads['source'] = value
        ffi.close()
        return downloads
    else:
        ffi = open(settings.DOWNLOAD_SET_PATTERN % os, 'rt')
        for line in ffi:
            ep = line.find('=')
            key = line[:ep].strip()
            value = line[ep+1:].strip()
            if key == 'MAC_DAILY':
                ffi.close()
                return {'mac': value}


@register.inclusion_tag('download_windows.html')
def download_win():
    return download_choices('win')


@register.inclusion_tag('download_mac-os-x.html')
def download_mac():
    return download_choices('mac')


@register.inclusion_tag('download_source.html')
def download_source():
    """Source data is in 'filenames_win.set'"""
    return download_choices('win')


@register.inclusion_tag('download_addons_win.html')
def download_addons_win():
    """Source data is in 'filenames_win.set'"""
    return download_choices('win')


@register.simple_tag
def download_link(os):
    if os == 'windows':
        return download_choices('win')['winw27']
    elif os == 'mac-os-x':
        return download_choices('mac')['mac']
    else:
        return download_choices('win')['source']
