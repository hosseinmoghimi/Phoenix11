
from pathlib import Path
from . import server_settings
import os
BASE_DIR = Path(__file__).resolve().parent.parent


 
DB_PREFIX_NAME='dikoo24ir'

CURRENCY='ریال'
DEBUG = False
DEBUG = True
DATABASE_NAME='20250723_23_35_38'

SITE_URL="/"
PUBLIC_ROOT="d:\\public_html\\phoenix11\\"
PRIVATE_ROOT="d:\\private_html\\phoenix11\\"

FULL_SITE_URL='http://127.0.0.1:8011/'

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'sth here'

DB_FILE_NAME=DB_PREFIX_NAME+'__'+DATABASE_NAME 
DB_FILE_PATH=os.path.join(BASE_DIR,DB_FILE_NAME+'.sqlite3')
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_FILE_PATH ,
    }
}
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'django_social_share',
    'tinymce',
    'core',
    'utility',
    'market',
    'accounting',
    'authentication',
    'processmanagement',
    'organization',
    'attachments',
    'projectmanager',
    'log',
    'chef',
    'school',
    'warehouse',
    'transport',
]
 



TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'



QRCODE_URL =SITE_URL+"qrcode/"
STATIC_URL =SITE_URL+"static/"

TEMPORARY_ROOT =os.path.join(PRIVATE_ROOT,"temp")
UPLOAD_ROOT =os.path.join(PRIVATE_ROOT,"upload")
QRCODE_ROOT =os.path.join(PUBLIC_ROOT,"qrcode")
STATIC_ROOT =os.path.join(PUBLIC_ROOT,"static")
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]

MEDIA_URL =SITE_URL+"media/"
MEDIA_ROOT =os.path.join(PUBLIC_ROOT,"media")

ADMIN_URL=SITE_URL+"admin/"


PUSHER_IS_ENABLE=False

VUE_VERSION_3=False
VUE_VERSION_2=True