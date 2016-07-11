"""Here we define custom django tags"""
import logging
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


@register.inclusion_tag('feed_results.html')
def grab_feed_all():
    """Grabs an RSS/Atom feed. Django will cache the content."""
    url = 'http://{0}/?feed=rss2'.format(settings.BLOG_HOST)
    feed = feedparser.parse(url)
    if feed.bozo == 0:
        # Parses first 3 entries from remote blog feed.
        entries = []
        for i in range(3):
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


def download_set_patterns(os=None):
    if path.isdir(settings.DOWNLOAD_DIR):
        if os is None:
            filename = path.join(settings.DOWNLOAD_DIR, "filenames.set")
        else:
            filename = settings.DOWNLOAD_SET_PATTERN % os

        if not path.isfile(filename):
            return

        with open(filename, 'rt') as f:
            for line in f:
                key, value = line.split('=', 1)
                yield key.strip(), value.strip()


def download_choices(os='win'):
    downloads = {}

    if os == 'win':
        for key, value in download_set_patterns(os):
            if key == 'WIN_SNAPSHOT':
                downloads['win27'] = '{0}-py2.7.exe'.format(value)
            elif key == 'WIN_PYTHON_SNAPSHOT':
                downloads['winw27'] = '{0}-py2.7.exe'.format(value)
            elif key == 'ADDON_BIOINFORMATICS_SNAPSHOT':
                downloads['bio27'] = '{0}-py2.7.exe'.format(value)
            elif key == 'ADDON_TEXT_SNAPSHOT':
                downloads['text27'] = '{0}-py2.7.exe'.format(value)
            elif key == 'SOURCE_SNAPSHOT':
                downloads['source'] = value

        for key, value in download_set_patterns(None):
            if key == "WIN32_ORANGE3_DAILY":
                downloads["orange3-win32-installer"] = value
            elif key == "WIN32_ORANGE3_STANDALONE_DAILY":
                downloads["orange3-win32-installer-standallone"] = value

    elif os == "mac":
        for key, value in download_set_patterns(os):
            if key == 'MAC_DAILY':
                downloads['mac'] = value
            if key == 'MAC_ORANGE3_DAILY':
                downloads['bundle-orange3'] = value
                try:
                    downloads['version'] = \
                        re.findall("Orange3-(.*)\.dmg", value)[0]
                except IndexError:  
                    downloads['version'] = 'unknown'
    else:
        for key, value in download_set_patterns('win'):
            if key == 'WIN_SNAPSHOT':
                downloads['date'] = value[-10:]

    return downloads


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
        return download_choices('win').get('winw27', '')
    elif os == 'mac-os-x':
        return download_choices('mac').get('mac', '')
    elif os == 'linux':
        return download_choices('win').get('source', '')
    else:
        return download_choices('date').get('date', '')


@register.simple_tag
def orange3_bundle_url():
    download_folder = reverse('download') + 'files/'
    orange3_bundle = download_choices('mac').get('bundle-orange3', '')
    return download_folder + orange3_bundle


@register.simple_tag
def orange3_win32_installer_url():
    download_folder = reverse('download') + 'files/'
    filename = download_choices('win').get('orange3-win32-installer', '')
    return download_folder + filename


@register.simple_tag
def orange2_bundle_url():
    download_folder = reverse('download') + 'files/'
    orange2_bundle = download_choices('mac').get('mac', '')
    return download_folder + orange2_bundle


@register.simple_tag
def orange2_win32_installer_url():
    download_folder = reverse('download') + 'files/'
    filename = download_choices('win').get('winw27', '')
    return download_folder + filename


@register.simple_tag
def orange2_source_url():
    download_folder = reverse('download') + 'files/'
    filename = download_choices('win').get('source', '')
    return download_folder + filename


def addonsget(searchtag):
    addons = []
    client = xmlrpclib.ServerProxy('http://pypi.python.org/pypi')
    try:
        slist = client.search({'keywords': searchtag})
        packages = sorted(set(a["name"] for a in slist))
        for iid, package in enumerate(packages):
            url = 'https://pypi.python.org/pypi/{0}/json'.format(package)
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
            if dl_url:
                if 'bitbucket' in dl_url and dl_url.endswith('/downloads'):
                    new_json['repo_url'] = dl_url[:-10]
                elif 'github' in dl_url and dl_url.endswith('/releases'):
                    new_json['repo_url'] = dl_url[:-9]
            addons.append(new_json)
        return addons
    except Exception as ex:
        logger.exception(ex)


@register.inclusion_tag('download_addons.html')
def download_addons():
    return {'addons': addonsget("orange3 add-on")}


@register.inclusion_tag('toolbox_widgets.html')
def toolbox_widgets(widget_js):
    return {'toolbox': widget_js}


@register.inclusion_tag('download_addons2.html')
def download_addons2():
    return {'addons': addonsget("orange add-on")}


@register.inclusion_tag('testimonials.html')
def testimonials_tag(data):
    return {'testimonials': data}
