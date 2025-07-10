
from pathlib import Path
from . import server_settings
import os


BASE_DIR = Path(__file__).resolve().parent.parent
 


CURRENCY='ریال'
DEBUG = False
DEBUG = True
VUE_VERSION_3=False
VUE_VERSION_2=True
DATABASE_NAME='phoenix11_20250705'

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'sth here'

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
]
 

DB_FULL_NAME=os.path.join(BASE_DIR,'db_'+DATABASE_NAME+'.sqlite3')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_FULL_NAME ,
    }
}


TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'



SITE_URL="/"
PUBLIC_ROOT="d:\\public_html\\phoenix11\\"
PRIVATE_ROOT="d:\\private_html\\phoenix11\\"

QRCODE_URL =SITE_URL+"qrcode/"
STATIC_URL =SITE_URL+"static/"

UPLOAD_ROOT =os.path.join(PRIVATE_ROOT,"upload")
QRCODE_ROOT =os.path.join(PUBLIC_ROOT,"qrcode")
STATIC_ROOT =os.path.join(PUBLIC_ROOT,"static")
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]

MEDIA_URL =SITE_URL+"media/"
MEDIA_ROOT =os.path.join(PUBLIC_ROOT,"media")

ADMIN_URL=SITE_URL+"admin/"
FULL_SITE_URL='http://127.0.0.1:8011/'


