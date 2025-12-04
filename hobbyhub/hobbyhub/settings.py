import os
import environ
from pathlib import Path


# BASE_DIR points to the root of your project.
# Django uses it to build absolute paths for templates, static files, media files, etc.
BASE_DIR = Path(__file__).resolve().parent.parent



# Initialize the environment reader.
# This lets us safely access environment variables using env("VAR_NAME").
env = environ.Env()

# Load variables from the .env file into the environment.
# Needed for local development so SECRET_KEY, DEBUG, DATABASE_URL, etc. work.
environ.Env.read_env()

# Load the .env file located in the project root.
# Using BASE_DIR ensures Django always finds the correct .env path.
environ.Env.read_env(BASE_DIR / '.env')



# Get SECRET_KEY from environment instead of hard-coding it.
# This is required for security and deployment on Fly.io.
SECRET_KEY = env('SECRET_KEY')


# DEBUG mode:
# - Reads the value from the .env file during local development.
# - Defaults to False for safety so production never accidentally runs with DEBUG=True.
DEBUG = env.bool('DEBUG', default=False)




APP_NAME = os.environ.get("FLY_APP_NAME")
ALLOWED_HOSTS = [ 
    "localhost",
    "127.0.0.1",
    f"{APP_NAME}.fly.dev"
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{APP_NAME}.fly.dev",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'accounts',
    'hobbies',
    'hobby_sessions',
    'friends',
    'encouragement_notes',
    'emoji_picker',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hobbyhub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hobbyhub.wsgi.application'



# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    "default": env.db(
         "DATABASE_URL", 
         default="sqlite:///db.sqlite3"
    )
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'





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

LOGIN_URL='/hobbyhub/login'


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

DEFAULT_CHARSET = 'utf-8'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_TZ = True




# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'




# MEDIA_URL = '/media/'          # tells the browser: “look under /media/ to load user-uploaded files

# MEDIA_ROOT = "/code/media"

# MEDIA_ROOT = BASE_DIR /'media'       # tells Django to store all uploaded files in a folder named media/ inside the project’s base directory

if os.environ.get("FLY_APP_NAME"):
    # Running on Fly.io
    MEDIA_ROOT = "/data/media"
    MEDIA_URL = "/media/"
else:
    # Local dev
    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"
