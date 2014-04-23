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
        'img': node.getAttribute('img') or ('homepage/screenshots/snp-%s.png' % iid),
        'rank': int(node.getAttribute('rank') or 999),
        'thumb': node.getAttribute('thumb') or ('homepage/screenshots/tbn-%s.png' % iid),
        'features': node.getAttribute('features'),
    }
    if not screenshot['hide'] == 'yes':
        _screenshots.append(screenshot)


def screenshots(request):
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
    if request.method == 'POST' and request.POST['signature'] == "I AGREE":
        message = "This message was sent to you automatically from orange.biolab.si.\n\n" + \
                  request.POST['fullname'] + " has agreed to and electronically signed Orange Contributor " \
                  "License Agreement. Below are his/her contact information:" \
                  "\n\nFull Name: " + request.POST['fullname'] + \
                  "\nE-mail: " + request.POST['email'] + \
                  "\nMailing Address: \n\n" + request.POST['address'] + \
                  "\n\nCountry: " + request.POST['country'] + \
                  "\nTelephone Number: " + request.POST['number'] + \
                  "\n\nThe user has agreed to electronically sign the agreement by typing I AGREE in the appropriate " \
                  "Electronic Signature form field.\n\nGood day,\nBiolab Webmaster"
        send_mail('Orange Contributor License Agreement Receipt', message, 'from@example.com',
                  ['mjenko@t-2.net'], fail_silently=False)
    return render(request, 'contributing-to-orange.html')


entries = []
feed = feedparser.parse('http://orange.biolab.si/blog/rss/')
for i in range(5):
    # Parses first 5 entries from remote blog feed.
    entry = {
        'title': feed['entries'][i]['title'],
        'link': feed['entries'][i]['link']
    }
    entries.append(entry)


def index(request):
    return render(request, 'homepage.html', {'blog': entries,
                                             'random_screenshots': random.sample(_screenshots, 4)})
