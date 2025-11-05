from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = '/outputs/'
MEDIA_ROOT = BASE_DIR / "outputs"
STATIC_URL = '/static/'

# === NETLIFY DETECTION ===
ON_NETLIFY = os.environ.get("NETLIFY") == "true"

SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
DEBUG = False
ALLOWED_HOSTS = ["*"]

# === APPS (middleware removed!) ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'village_app',
]

# === ONLY ADD GeoDjango when NOT on Netlify ===
if not ON_NETLIFY:
    INSTALLED_APPS.append('django.contrib.gis')

# === MIDDLEWARE (whitenoise moved HERE) ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← CORRECT PLACE
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'rural_dev.urls'

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

WSGI_APPLICATION = 'rural_dev.wsgi.application'

# === DATABASE (ignored on Netlify) ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
