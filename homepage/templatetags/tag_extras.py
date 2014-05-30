"""Here we define custom django tags"""
from datetime import datetime as dt

from django import template
from docutils.core import publish_parts
from django.conf import settings

import feedparser
import requests
import xmlrpclib

register = template.Library()


@register.inclusion_tag('feed_results.html')
def grab_feed_all():
    """Grabs an RSS/Atom feed. Django will cache the content."""
    url = 'http://' + settings.ALLOWED_HOSTS[0] + '/blog/rss/'
    feed = feedparser.parse(url)
    if feed.bozo == 0:
        # Parses first 6 entries from remote blog feed.
        entries = []
        for i in range(6):
            pub_date = feed['entries'][i]['published'][:-6]
            df = '%a, %d %b %Y %H:%M:%S'
            entry = {
                'title': feed['entries'][i]['title'],
                'link': feed['entries'][i]['link'],
                'published': dt.strptime(pub_date, df).strftime('%d %b'),
            }
            entries.append(entry)
        return {'entries': entries,
                'bozo': False
                }
    else:
        return {'bozo': True}


# Custom tab for grabbing the first post from Orange blog RSS
#
# @register.inclusion_tag('first_feed_result.html')
# def grab_feed_first():
#     """Grabs an RSS/Atom feed. Django will cache the content."""
#     url = 'http://' + settings.ALLOWED_HOSTS[0] + '/blog/rss/'
#     feed = feedparser.parse(url)
#     if feed.bozo == 0:
#         # Parses first entry from remote blog feed.
#         return {'title': feed['entries'][0]['title'],
#                 'link': feed['entries'][0]['link'],
#                 'text': feed['entries'][0]['summary_detail']['value'],
#                 'bozo': False
#                 }
#     else:
#         return {'bozo': True}


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
            if key == 'WIN_SNAPSHOT':
                value = line[ep+1:].strip()
                downloads['win25'] = '%s-py2.5.exe' % value
                downloads['win26'] = '%s-py2.6.exe' % value
                downloads['win27'] = '%s-py2.7.exe' % value
            elif key == 'WIN_PYTHON_SNAPSHOT':
                value = line[ep+1:].strip()
                downloads['winw25'] = '%s-py2.5.exe' % value
                downloads['winw26'] = '%s-py2.6.exe' % value
                downloads['winw27'] = '%s-py2.7.exe' % value
            elif key == 'ADDON_BIOINFORMATICS_SNAPSHOT':
                value = line[ep+1:].strip()
                downloads['bio26'] = '%s-py2.6.exe' % value
                downloads['bio27'] = '%s-py2.7.exe' % value
            elif key == 'ADDON_TEXT_SNAPSHOT':
                value = line[ep+1:].strip()
                downloads['text26'] = '%s-py2.6.exe' % value
                downloads['text27'] = '%s-py2.7.exe' % value
            elif key == 'SOURCE_SNAPSHOT':
                value = line[ep+1:].strip()
                downloads['source'] = value
        ffi.close()
        return downloads
    if os == "mac":
        ffi = open(settings.DOWNLOAD_SET_PATTERN % os, 'rt')
        for line in ffi:
            ep = line.find('=')
            key = line[:ep].strip()
            if key == 'MAC_DAILY':
                value = line[ep+1:].strip()
                ffi.close()
                return {'mac': value}
    else:
        ffi = open(settings.DOWNLOAD_SET_PATTERN % "win", 'rt')
        for line in ffi:
            ep = line.find('=')
            key = line[:ep].strip()
            if key == 'WIN_SNAPSHOT':
                value = line[ep+1:].strip()[-10:]
                ffi.close()
                return {'date': value}


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
    elif os == 'linux':
        return download_choices('win')['source']
    else:
        return download_choices('date')['date']


@register.inclusion_tag('download_addons.html')
def download_addons():
    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    addons = []
    for iid, package in enumerate(client.search({'keywords': 'orange'})):
        # TODO: Possible threaded URL fetching
        url = 'https://pypi.python.org/pypi/' + package['name'] + '/json'
        r = requests.get(url)
        jsonfile = r.json()
        desc = jsonfile['info']['description'].split('\n')
        # RST -> HTML conversion
        desc = publish_parts('\n'.join(desc[3:]), writer_name='html')
        new_json = {
            'iid': iid + 1,
            'name': jsonfile['info']['name'],
            'version': jsonfile['info']['version'],
            'description': desc['html_body'],
            'package_url': jsonfile['info']['package_url'],
            'download_url': jsonfile['info']['download_url'],
            'repo_url': None,
            'docs_url': jsonfile['info']['docs_url'],
            'home_page': jsonfile['info']['home_page'],
        }
        dl_url = jsonfile['info']['download_url']
        if "bitbucket" in dl_url and dl_url.endswith('/downloads'):
            new_json['repo_url'] = dl_url[:-10]
        elif "github" in dl_url and dl_url.endswith('/releases'):
            new_json['repo_url'] = dl_url[:-9]
        addons.append(new_json)
    return {'addons': addons}
