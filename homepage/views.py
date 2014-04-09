import xml.dom.minidom

from django.shortcuts import render
from django.conf import settings
# from django.template import RequestContext, loader


doc = xml.dom.minidom.parse(file(settings.SCREENSHOTS_INDEX))

def screenshots(request):
	screenshots = []
	for node in doc.getElementsByTagName('screenshot'):
		id = node.getAttribute('id')
		screenshot = {
		'id': id,
		'title': node.getAttribute('title'),
		'hide': node.getAttribute('hide'),
		'img': node.getAttribute('img') or ('/static/homepage/screenshots/snp-%s.png' % id),
		'rank': int(node.getAttribute('rank') or 999),
		'thumb': node.getAttribute('thumb') or ('/static/homepage/screenshots/tbn-%s.png' % id),
		'features': node.getAttribute('features'),
		}
		if not screenshot['hide'] == 'yes':
			screenshots.append(screenshot)
	screenshots.sort(key=lambda x: x['rank'])
	return render(request, 'screenshots.html', {'screenshots': screenshots})

# class LicensePlugin(CMSPluginBase):
#     """
#     Displays a license file.
#     """
# def render(self, context, instance, placeholder):
# return context

f=file(settings.LICENSE_INDEX)

def license(request):
	# name = _('License file')
	# render_template = 'main/license.html'
	in_other = False
	text = ""
	other = []
	for l in f:
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


def index(request):
	return render(request, 'homepage.html')