import os
from pathlib import Path
from datetime import timedelta
import django_heroku
import firebase_admin
from firebase_admin import credentials
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', "django-insecure-9$f)szk-3$+lrq__0rjxq+jab7q&8wq%jt0l7n^ayos7o^r#8b")

DEBUG = bool(os.environ.get('DEBUG', True))
DB_PATH = os.environ.get('DB_PATH', '')
ALLOWED_HOSTS = ['.herokuapp.com', 'localhost', '127.0.0.1']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'marketplace',
    'cloudinary',
    'cloudinary_storage',
    'corsheaders'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]

CORS_ALLOW_ALL_ORIGINS = True  

ROOT_URLCONF = "piggy.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = "piggy.wsgi.application"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}



DATABASES = {
    'default': dj_database_url.config(default=DB_PATH)
}


AUTH_USER_MODEL = 'marketplace.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



LANGUAGE_CODE = 'fr-FR'  # Or another language supporting accented characters
TIME_ZONE = 'UTC'  # Or your desired timezone
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'votre_cloud_name',
    'API_KEY': 'votre_api_key',
    'API_SECRET': 'votre_api_secret',
}

CLOUDINARY_CLOUD_NAME = 'votre_nom_de_cloud'
CLOUDINARY_API_KEY = 'votre_clé_api'
CLOUDINARY_UPLOAD_PRESET = 'votre_preset_de_téléchargement'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

cred = credentials.Certificate(os.path.join(BASE_DIR, 'serviceAccountKey.json'))
firebase_admin.initialize_app(cred)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

django_heroku.settings(locals())

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
