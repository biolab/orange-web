from orange_web.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['orange.biolab.si', 'new.orange.biolab.si']
DOWNLOAD_SET_PATTERN = os.path.join('/srv/download', 'filenames_%s.set')

SECRET_KEY = '#$%&#ZE$W%$GTZ&%U)hwd#(**#&/(/hG&%EfSDrtzbjtverwe4$Q$juktHR&//ZreCFSWERWXEDasdfgwc#dawaDGA$o4e'
RECAPTCHA_SECRET = '6Lemwf4SAAAAAGOkKhoiGbMGwoLoYT840IsGjwab'
