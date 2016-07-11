import json
import xml.dom.minidom

from django.conf import settings


# Create a list of admin e-mail addresses.
ADMINS = [x[1] for x in settings.ADMINS]


# Find and create a list of screenshots
def discover_screenshots():
    f = open(settings.SCREENSHOTS_INDEX)
    doc = xml.dom.minidom.parse(f)
    f.close()

    s_shots = []
    for node in doc.getElementsByTagName('screenshot'):
        iid = node.getAttribute('id')
        s_shot = {
            'id': iid,
            'title': node.getAttribute('title'),
            'hide': node.getAttribute('hide'),
            'img': 'homepage/screenshots/images/%s.png' % iid,
            'rank': int(node.getAttribute('rank') or 999),
            'thumb': 'homepage/screenshots/images/%s-thumb.png' % iid,
            'features': node.getAttribute('features'),
        }
        s_shots.append(s_shot)
    return s_shots

SCREENSHOTS = [screen for screen in discover_screenshots()
               if not screen['hide'] == 'yes']


# Load features catalog, pass it to homepage.html template
try:
    with open(settings.FEATURES_CATALOG, "rt") as fp:
        FEATURE_DESCRIPTIONS = json.load(fp)
except IOError:
    FEATURE_DESCRIPTIONS = []


# Load testimonials catalog, pass it to testimonials.html template
try:
    with open(settings.TESTIMONIALS_CATALOG, "rt") as fp:
        TESTIMONIALS = json.load(fp)
except IOError:
    TESTIMONIALS = []

# Load widgets catalog, pass it to toolbox.html template
try:
    with open(settings.WIDGET_CATALOG, "rt") as fp:
        WIDGET_JS = json.load(fp)
except IOError:
    WIDGET_JS = []
# For use with TrieSearch in Widgets Catalog (convenience, performance util)
WIDG_JS = {}
widget_idx = 0
for field_key, field_val in WIDGET_JS:
    for widget in field_val:
        # Widget name
        WIDG_JS[widget['text']] = widget_idx
        # Widget keywords
        for keyword in widget.get('keywords', ()):
            WIDG_JS[keyword] = widget_idx
        widget_idx += 1

# Load license file
try:
    with open(settings.LICENSE_FILE) as fl:
        LICENSE = fl.readlines()
except IOError:
    LICENSE = ['', ]
