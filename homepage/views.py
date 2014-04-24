import xml.dom.minidom
import random

from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail

import feedparser

f = open(settings.SCREENSHOTS_INDEX)
doc = xml.dom.minidom.parse(f)
f.close()

_screenshots = []
for node in doc.getElementsByTagName('screenshot'):
    iid = node.getAttribute('id')
    screenshot = {
        'id': iid,
        'title': node.getAttribute('title'),
        'hide': node.getAttribute('hide'),
        'img': node.getAttribute('img')
        or ('homepage/screenshots/snp-%s.png' % iid),
        'rank': int(node.getAttribute('rank') or 999),
        'thumb': node.getAttribute('thumb')
        or ('homepage/screenshots/tbn-%s.png' % iid),
        'features': node.getAttribute('features'),
    }
    if not screenshot['hide'] == 'yes':
        _screenshots.append(screenshot)


def screenshots(request):
    """Sort screenshots by their rank, put them into a list of clusters of 4"""
    _screenshots.sort(key=lambda x: x['rank'])
    return render(request, 'screenshots.html', {'screenshots': _screenshots})


fl = open(settings.LICENSE_FILE)
license_file = fl.readlines()
fl.close()


def license(request):
    text = ""
    in_other = False
    other = []
    for l in license_file:
        if l.startswith('----'):
            in_other = not in_other
            if in_other:
                other.append(l)
            else:
                other[-1] += l.rstrip()
        elif in_other:
            other[-1] += l
        else:
            text += l
    context = {
        'text': text,
        'other': other,
    }
    return render(request, 'license.html', context)


def contribute(request):
    if request.method == 'POST' and request.POST['Signature'] == "I AGREE":
        message = "This message was sent to you automatically from orange.biolab.si.\n\n" + \
                  request.POST['Full Name'] + " electronically signed Orange Contributor " \
                  "License Agreement. Below are his/her contact information:" \
                  "\n\nFull Name: " + request.POST['Full Name'] + \
                  "\nE-mail: " + request.POST['E-mail'] + \
                  "\nMailing Address: \n\n" + request.POST['Address'] + \
                  "\n\nCountry: " + request.POST['Country'] + \
                  "\nTelephone Number: " + request.POST['Number'] + \
                  "\n\nThe user has confirmed this action by typing " \
                  "\"I AGREE\" in the appropriate Electronic Signature form field." \
                  "\n\nGood day,\nBiolab Webmaster"
        send_mail('Orange Contributor License Agreement Receipt', message,
                  'from@example.com', ['mjenko@t-2.net'], fail_silently=False)
    return render(request, 'contributing-to-orange.html')


feed = feedparser.parse('http://orange.biolab.si/blog/rss/')
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
        entries_2.append(entry)
    else:
        entries_1.append(entry)


def index(request):
    return render(request, 'homepage.html', {
        'entries_1': entries_1,
        'entries_2': entries_2,
        'random_screenshots': random.sample(_screenshots, 4)})


def download(request):
    return render(request, 'download.html')


def community(request):
    return render(request, 'download.html')
