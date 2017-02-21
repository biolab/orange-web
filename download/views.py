# Regex objects for browser OS detection
import re

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render

from homepage.templatetags.tag_extras import download_choices

p_win = re.compile(r'.*[Ww]in.*')
p_mac = re.compile(r'^(?!.*(iPhone|iPad)).*[Mm]ac.*')
p_linux = re.compile(r'.*[Ll]inux.*')


def detect_os(user_agent):
    if re.match(p_win, user_agent):
        return 'windows'
    elif re.match(p_mac, user_agent):
        return 'mac-os-x'
    elif re.match(p_linux, user_agent):
        return 'linux'
    else:
        return ''


def download(request, os=None):
    if os is None:
        landing_page = True
        os = detect_os(request.META.get('HTTP_USER_AGENT', ''))
    else:
        landing_page = False

    return render(request, 'download/base.html', dict(
        landing_page=landing_page,
        os=os,
        tabs=[
            dict(icon="windows", title="Windows", os="windows"),
            dict(icon="apple", title="macOS", os="mac-os-x"),
            dict(icon="linux", title="Linux / Source", os="linux"),
        ],
        recommended=recommended_download(os)
    ))


VERSION_RE = re.compile(r"Orange3-([\d\.]+)\.")


def recommended_download(os):
    downloads = download_choices()

    def get_version(filename):
        try:
            return VERSION_RE.findall(filename)[0]
        except IndexError:
            return "unknown"

    filename = title = ""
    if os == "windows":
        title = "Windows Installer"
        filename = downloads["orange3-win32-installer"]
    elif os == "mac-os-x":
        title = "macOS bundle"
        filename = downloads["bundle-orange3"]

    if filename:
        return dict(
            filename=filename,
            url=reverse('download') + 'files/' + filename,
            version=get_version(filename),
            title=title
        )
    else:
        return None


def latest_version(request):
    version = download_choices('mac').get('version', '')
    return HttpResponse(version, content_type="text/plain")
