 
from pathlib import Path
from . import server_settings 
BASE_DIR = Path(__file__).resolve().parent.parent 


SECRET_KEY=server_settings.SECRET_KEY
DEBUG=server_settings.DEBUG
ALLOWED_HOSTS=server_settings.ALLOWED_HOSTS
INSTALLED_APPS=server_settings.INSTALLED_APPS
SECRET_KEY=server_settings.SECRET_KEY



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'phoenix.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'core.views.CoreContext',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'phoenix.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = server_settings.DATABASES


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = server_settings.TIME_ZONE

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
 

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




LANGUAGE_CODE = server_settings.LANGUAGE_CODE

TIME_ZONE =server_settings.TIME_ZONE 

USE_I18N = True

USE_TZ = True


SITE_URL =server_settings.SITE_URL
PUBLIC_ROOT =server_settings.PUBLIC_ROOT

STATIC_URL =server_settings.STATIC_URL
STATIC_ROOT =server_settings.STATIC_ROOT
STATICFILES_DIRS =server_settings.STATICFILES_DIRS

MEDIA_URL =server_settings.MEDIA_URL
MEDIA_ROOT =server_settings.MEDIA_ROOT 

ADMIN_URL=server_settings.ADMIN_URL
 
FULL_SITE_URL=server_settings.FULL_SITE_URL
 

