import os

from settings import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

DOWNLOAD_SET_PATTERN = os.path.join('/srv/download', 'filenames_%s.set')

ALLOWED_HOSTS = ['orange.biolab.si', 'new.orange.biolab.si']
