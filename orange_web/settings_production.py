from orange_web.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['orange.biolab.si', 'new.orange.biolab.si', '193.2.72.56', 'qa.orange.biolab.si']
DOWNLOAD_DIR = '/srv/download'
WIDGET_CATALOG = '/srv/chroot_rsync/orange3doc/visual-programming/widgets.json'
ERROR_REPORT_DIR = '/srv/error_report/'
LOGGING_DIR = '/var/log/django/'

DOWNLOAD_SET_PATTERN = os.path.join(DOWNLOAD_DIR, 'filenames_%s.set')

# Django, reCaptcha secret keys
with open('/etc/orange_web.conf', 'r') as f:
    lines = f.readlines()
    SECRET_KEY = lines[0].split('=', 1)[1]
    RECAPTCHA_SECRET = lines[1].split('=', 1)[1]

# SMTP settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.fri.uni-lj.si'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(name)s %(filename)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR + 'django-info.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'root': {
        'handlers': ['file', 'mail_admins'],
        'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
    },
}
