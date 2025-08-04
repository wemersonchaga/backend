import os
from pathlib import Path
from dotenv import load_dotenv

# Base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega o .env
dotenv_path = BASE_DIR / '.env'
load_dotenv(dotenv_path)

# Segurança
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Hosts permitidos
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if 'CODESPACE_NAME' in os.environ:
    ALLOWED_HOSTS.append(f'{os.environ["CODESPACE_NAME"]}-8000.app.github.dev')
ALLOWED_HOSTS += [
    '20.119.97.89',
    'nannyspets-be-drc8ggc3d4c7hxfr.brazilsouth-01.azurewebsites.net',
    'nannys-backend.onrender.com',
    '*',  # Cuidado: só em desenvolvimento!
]

# CSRF trusted (ex: Render, Azure, Codespaces)
CSRF_TRUSTED_ORIGINS = [
    'https://localhost:8000',
    'https://127.0.0.1:8000',
    'https://nannys-backend.onrender.com',
    'https://nannyspets-be-drc8ggc3d4c7hxfr.brazilsouth-01.azurewebsites.net',
    'https://*.github.dev',
    'https://*.azurewebsites.net',
    'https://*.onrender.com',
]

# Data
DATE_FORMAT = 'd/m/Y'

# Aplicações
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'drf_yasg',
    'nanny_pets_app',
]

# Middleware
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS
CORS_ALLOW_ALL_ORIGINS = True  # Para dev. Em produção, defina `CORS_ALLOWED_ORIGINS`
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://20.119.97.89:8000',
    'https://nannyspets-be-drc8ggc3d4c7hxfr.brazilsouth-01.azurewebsites.net',
]

# URLs
ROOT_URLCONF = 'tutorial.urls'

# Templates
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

WSGI_APPLICATION = 'tutorial.wsgi.application'

# Banco de dados
USE_POSTGRES = os.getenv('USE_POSTGRES', 'False') == 'True'

if USE_POSTGRES:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'backend_db'),
            'USER': os.getenv('DB_USER', 'wemerson'),
            'PASSWORD': os.getenv('DB_PASSWORD', '1240'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Arquivos estáticos e mídia
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
}

# Libera Swagger sem login no modo DEBUG
if DEBUG:
    REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ['rest_framework.permissions.AllowAny']

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Digite: Token <seu_token>',
        }
    },
}

# Auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
