import os

import environ

from ._sensitive import manage_sensitive


root = environ.Path(__file__) - 3
env = environ.Env()
environ.Env.read_env('environments/docker.env')

BASE_DIR = root()

SECRET_KEY = manage_sensitive('SECRET_KEY')

DEBUG = env('DEBUG', default=False)

USE_S3_STORAGE = env('USE_S3_STORAGE', default=False)

STATIC_FILES_FOLDER_NAME = 'staticfiles'

MEDIA_FILES_FOLDER_NAME = 'mediafiles'

STATIC_URL = f'/{STATIC_FILES_FOLDER_NAME}/'

MEDIA_URL = f'/{MEDIA_FILES_FOLDER_NAME}/'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

STATIC_ROOT = os.path.join(BASE_DIR, STATIC_FILES_FOLDER_NAME)

MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_FILES_FOLDER_NAME)

if USE_S3_STORAGE:
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = manage_sensitive('AWS_SECRET_ACCESS_KEY')
    AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
    AWS_STORAGE_BUCKET_NAME = 'pets'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_SIGNATURE_VERSION = 's3v4'

    STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{STATIC_FILES_FOLDER_NAME}/'
    MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{MEDIA_FILES_FOLDER_NAME}/'
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

ALLOWED_HOSTS = [host for hosts in env.list('ALLOWED_HOSTS') for host in hosts.split(';')]
API_KEY = manage_sensitive('API_KEY')

API_KEY_CUSTOM_HEADER = 'HTTP_X_API_KEY'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_api_key',
    'storages',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'api.permissions.ApiKeyHeaderMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pets.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pets.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env('APP_DB_ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': manage_sensitive('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT')
    },
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
