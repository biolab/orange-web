import xml.dom.minidom
import random
import re
import requests
import json

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


# TODO: Leave secret only in settings_production
def pass_captcha(request):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    params = {
        'secret': '6Lemwf4SAAAAAGOkKhoiGbMGwoLoYT840IsGjwab',
        'response': request.POST.get('g-recaptcha-response')
    }
    r = requests.get(url, params=params)
    return json.loads(r.content).get('success')


def contribute(request):
    response = {'post': None}
    if request.method == 'POST':
        if not pass_captcha(request):
            response['post'] = -2
        elif request.POST['Signature'] != 'I AGREE':
            response['post'] = -1
        else:
            message = ('This message was sent to you automatically from orange.biolab.si.\n\n'
                       '{0} electronically signed Orange Contributor License Agreement. '
                       'Below are his/her contact information:\n\n'
                       'Full Name: {0}\n'
                       'E-mail: {1}\n'
                       'Mailing Address: \n\n{2}\n'
                       'Country: {3}\n'
                       'Telephone Number: {4}\n\n'
                       'The user has confirmed this action by typing "I AGREE" in the '
                       'appropriate Electronic Signature form field.\n\n'
                       'Good day,\n'
                       'Biolab Webmaster').format(request.POST['Full Name'],
                                                  request.POST['E-mail'],
                                                  request.POST['Address'],
                                                  request.POST['Country'],
                                                  request.POST['Number'])
            send_mail('Orange Contributor License Agreement Receipt', message,
                      request.POST['E-mail'], admins, fail_silently=True)
            response['post'] = 1
    return render(request, 'contributing-to-orange.html', response)

# TODO: This function
def contact(request):
    cap_ok = pass_captcha(request)

    response = {"post": False}
    if request.method == 'POST':
        # message = "This message was sent to you automatically from orange.biolab.si.\n\n" + \
        #           "A Contact form was submitted. Below are the details:" \
        #           "\n\nE-mail: " + request.POST['E-mail'] + \
        #           "\nSubject: " + request.POST['Subject'] + \
        #           "\nMessage: \n\n" + request.POST['Message'] + \
        #           "\n\nGood day,\nBiolab Webmaster"
        # send_mail('Orange Contact Request', message,
        #           request.POST['E-mail'], admins, fail_silently=False)
        response = {"post": True}
    return render(request, 'contact.html', response)

# Regex objects for browser OS detection
p_win = re.compile(r'.*[Ww]in.*')
p_mac = re.compile(r'^(?!.*(iPhone|iPad)).*[Mm]ac.*')
p_linux = re.compile(r'.*[Ll]inux.*')


def detect_os(user_agent):
    if re.match(p_win, user_agent):
        return "windows"
    elif re.match(p_mac, user_agent):
        return "mac-os-x"
    elif re.match(p_linux, user_agent):
        return "linux"
    else:
        return ""


def index(request):
    response = {
        'random_screenshots': random.sample(screenshots, 5),
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


def start(request):
    return render(request, 'start.html',
                  {'screens_root': 'homepage/getting_started'})
