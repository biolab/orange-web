from orange_web.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['orange.biolab.si', 'new.orange.biolab.si']
DOWNLOAD_SET_PATTERN = os.path.join('/srv/download', 'filenames_%s.set')
