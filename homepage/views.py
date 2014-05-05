import xml.dom.minidom
import random
import re

from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail

# Create a list of admin e-mail addresses.
admins = [x[1] for x in settings.ADMINS]


f = open(settings.SCREENSHOTS_INDEX)
doc = xml.dom.minidom.parse(f)
f.close()

screenshots = []
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
        screenshots.append(screenshot)


def screens(request):
    """Sort screenshots by their rank"""
    screenshots.sort(key=lambda x: x['rank'])
    return render(request, 'screenshots.html', {'screenshots': screenshots})


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
    response = {"post": None}
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
                  request.POST['E-mail'], admins, fail_silently=False)
        response = {"post": 1}
    elif request.method == 'POST' and request.POST['Signature'] != "I AGREE":
        response = {"post": -1}
    return render(request, 'contributing-to-orange.html', response)


def contact(request):
    response = {"post": False}
    if request.method == 'POST':
        message = "This message was sent to you automatically from orange.biolab.si.\n\n" + \
                  "A Contact form was submitted. Below are the details:" \
                  "\n\nE-mail: " + request.POST['E-mail'] + \
                  "\nSubject: " + request.POST['Subject'] + \
                  "\nMessage: \n\n" + request.POST['Message'] + \
                  "\n\nGood day,\nBiolab Webmaster"
        send_mail('Orange Contact Request', message,
                  request.POST['E-mail'], admins, fail_silently=False)
        response = {"post": True}
    return render(request, 'contact.html', response)


def detect_os(user_agent):
    if re.match(r'.*[Ww]in.*', user_agent):
        return "windows"
    elif re.match(r'^(?!.*(iPhone|iPad)).*[Mm]ac.*', user_agent):
        return "mac-os-x"
    elif re.match(r'.*[Ll]inux.*', user_agent):
        return "linux"
    else:
        return ""


def index(request):
    response = {
        'random_screenshots': random.sample(screenshots, 4),
        'os': detect_os(request.META['HTTP_USER_AGENT'])
    }
    return render(request, 'homepage.html', response)


def download(request, os=None):
    os_response = {'os': None}
    if os is None:
        os_response['os'] = detect_os(request.META['HTTP_USER_AGENT'])
    else:
        os_response['os'] = os
    return render(request, 'download.html', os_response)
