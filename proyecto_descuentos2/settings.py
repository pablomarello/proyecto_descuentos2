"""
Django settings for proyecto_descuentos2 project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from decouple import config
from django.contrib.messages import constants as mensajes_error

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['localhost','127.0.0.1']

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuario',
    'persona',
    'oferente',
    'producto',
    'oferta',
    'django_recaptcha',
    'django_select2',
    'django_extensions',
    'estadistica',
    'rest_framework',
    'administracion',
    'chatbot',
    
]

#crispy tailwind css settings
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
    'proyecto_descuentos2.middleware.RedirectUnauthenticatedMiddleware',
    
]

ROOT_URLCONF = 'proyecto_descuentos2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'usuario.context_processors.base_categorias',
                'usuario.context_processors.comercio_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'proyecto_descuentos2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

#Base de datos DE MICA? -_-
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),  # Conviértelo a entero
    },
    'supabase': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('SUPABASE_DB_NAME'),
        'USER': config('SUPABASE_DB_USER'),
        'PASSWORD': config('SUPABASE_DB_PASSWORD'),
        'HOST': config('SUPABASE_DB_HOST'),
        'PORT': config('SUPABASE_DB_PORT', cast=int),
        'OPTIONS': {
          'sslmode': 'verify-full',
          'sslrootcert': config('SSL_ROOT_CERT')

        }
    }
}  



""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'DB_HOST',
        'PORT': 'DB_PORT',
    }
}
 """

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
#indicamos el modelo de usuario personalizado que queremos utilizar
AUTH_USER_MODEL = 'usuario.Usuario'

LOGIN_REDIRECT_URL='index'


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Buenos_Aires'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR, "staticfiles")

#donde se alojan los archivos estaticos
STATICFILES_DIRS = (os.path.join(BASE_DIR,'static'),)


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

MEDIA_URL = '/media/' #url publica que aparecera en la barra del navegador
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') #donde buscará los archivos media

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CRISPY FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MESSAGE_TAGS= {
    mensajes_error.DEBUG: 'debug',
    mensajes_error.INFO: 'info',
    mensajes_error.SUCCESS: 'success',
    mensajes_error.WARNING: 'warning',
    mensajes_error.ERROR: 'danger',
}

#datos del correo
EMAIL_BACKEND=config("EMAIL_BACKEND")
EMAIL_HOST=config("EMAIL_HOST")
EMAIL_PORT=config("EMAIL_PORT")
EMAIL_USE_TLS=config("EMAIL_USE_TLS")
EMAIL_HOST_USER=config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD=config("EMAIL_HOST_PASSWORD")

#ReCaptcha
API_KEY = 'AIzaSyD8I6b-GtswsS4OvckuRcXwcPt60SnV2Wk'

SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']


RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_USE_SSL = True


#datos de los sms
Apy_telefono=config('apykey')