import os
import xml.dom.minidom

from django.shortcuts import render
from django.conf import settings
# from django.template import RequestContext, loader


class Screenshot(object):
	def __init__(self, **argv):
		self.__dict__.update(argv)

doc = xml.dom.minidom.parse(file(settings.SCREENSHOTS_INDEX))
def screenshots(request):
	screenshots = []
	features_screenshots = []
	for node in doc.getElementsByTagName('screenshot'):
		id = node.getAttribute('id')
		screenshot = {
			'id': id,
			'title': node.getAttribute('title'),
			'hide': node.getAttribute('hide'),
			# 'img': node.getAttribute('img') or os.path.join(settings.SCREENSHOTS_DIR,'snp-%s.png' % id),
		    'img': node.getAttribute('img') or ('/static/homepage/screenshots/snp-%s.png' % id),
			'rank': int(node.getAttribute('rank') or 999),
		    'thumb':node.getAttribute('thumb') or ('/static/homepage/screenshots/tbn-%s.png' % id),
			# 'thumb':node.getAttribute('thumb') or os.path.join(settings.SCREENSHOTS_DIR,'tbn-%s.png' % id),
			'features': node.getAttribute('features'),
		}
		if not screenshot['hide'] == 'yes':
			screenshots.append(screenshot)
		# if features:
		# 	features_screenshots.append(
		# 		(rank, Screenshot(id=id, img=img, rank=rank, thumb=thumb, title=title, features=features)))
	# screenshots = [s for _, s in sorted(screenshots)]
	# features_screenshots = [s for _, s in sorted(features_screenshots)]
	return render(request,'screenshots.html', {'screenshots': screenshots})


def index(request):
	return render(request, 'homepage.html')