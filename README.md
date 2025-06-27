# Phoenix11



server_settings.py
copy from here

```bash 

from pathlib import Path
from . import server_settings
import os


BASE_DIR = Path(__file__).resolve().parent.parent
 


CURRENCY='ریال'
DEBUG = False
DEBUG = True
VUE_VERSION_3=False
VUE_VERSION_2=True
DATABASE_NAME='phoenix11_20250527'

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
    'log',
    'chef',
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

```


server_apps.py

```
from .server_settings import SITE_URL,STATIC_URL

phoenix_apps=[
    {'priority':1,'name':'core','url':SITE_URL+'','title':'خانه','logo':STATIC_URL+'core'+'/img/'+'logo.png','color':'warning',},
    {'priority':2,'name':'accounting','url':SITE_URL+'accounting/','title':'حسابداری','logo':STATIC_URL+'accounting'+'/img/'+'logo.png','color':'success',},
    {'priority':3,'name':'market','url':SITE_URL+'market/','title':'فروشگاه','logo':STATIC_URL+'market'+'/img/'+'logo.png','color':'success',},
    {'priority':4,'name':'authentication','url':SITE_URL+'authentication/','title':'هویت','logo':STATIC_URL+'authentication'+'/img/'+'logo.png','color':'success',},
    # {'priority':5,'name':'processmanagement','url':SITE_URL+'processmanagement/','title':'مدیریت فرآیند','logo':STATIC_URL+'processmanagement'+'/img/'+'logo.png','color':'success',},
    {'priority':5,'name':'utility','url':SITE_URL+'utility/','title':'ابزار های کاربردی','logo':STATIC_URL+'utility'+'/img/'+'logo.png','color':'success',},
    {'priority':6,'name':'log','url':SITE_URL+'log/','title':'لاگ','logo':STATIC_URL+'log'+'/img/'+'logo.png','color':'success',},
    {'priority':7,'name':'chef','url':SITE_URL+'chef/','title':'سرآشپز','logo':STATIC_URL+'chef'+'/img/'+'logo.png','color':'success',},
   
   
]
```


server_urls.py
```
from django.urls import path,include,re_path
from django.views.static import serve
from phoenix.server_settings import QRCODE_ROOT,STATIC_ROOT,MEDIA_ROOT
urlpatterns = [ 
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('log/', include('log.urls')),
    path('authentication/', include('authentication.urls')),
    path('accounting/', include('accounting.urls')),
    path('market/', include('market.urls')),
    path('chef/', include('chef.urls')),
    path('utility/', include('utility.urls')),
    
    
    
    re_path(r'^qrcode/(?P<path>.*)$', serve, {'document_root': QRCODE_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),


]

```



settings_on_servers.py

```

# from .enums import AccountTypeEnum
from django.db.models import TextChoices
from django.utils.translation import gettext as _
from utility.log import leolog


NO_DUPLICATED_ACCOUNT_NAME=True
NO_DUPLICATED_ACCOUNT_CODE=True 

class AccountTypeEnum(TextChoices):
    GROUP='گروه',_('گروه')
    BASIC='کل',_('کل')
    MOEIN_1='معین 1',_('معین 1')
    MOEIN_2='معین 2',_('معین 2')
    TAFSILI_1='تفصیلی 1',_('تفصیلی 1')
    TAFSILI_2='تفصیلی 2',_('تفصیلی 2')
    TAFSILI_3='تفصیلی 3',_('تفصیلی 3')
    TAFSILI_4='تفصیلی 4',_('تفصیلی 4')
    TAFSILI_5='تفصیلی 5',_('تفصیلی 5')
    TAFSILI_6='تفصیلی 6',_('تفصیلی 6')


ACCOUNT_LEVEL_NAMES= [
    AccountTypeEnum.GROUP,
    AccountTypeEnum.BASIC,
    AccountTypeEnum.MOEIN_1,
    AccountTypeEnum.MOEIN_2,
    AccountTypeEnum.TAFSILI_1,
    AccountTypeEnum.TAFSILI_2,
    AccountTypeEnum.TAFSILI_3,
    AccountTypeEnum.TAFSILI_4,
    AccountTypeEnum.TAFSILI_5,
    AccountTypeEnum.TAFSILI_6,
]
 
```