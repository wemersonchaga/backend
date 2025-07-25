"""
Django settings for tutorial project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from rest_framework.permissions import AllowAny

# Define o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega variáveis de ambiente do arquivo .env no BASE_DIR
dotenv_path = BASE_DIR / '.env'
load_dotenv(dotenv_path)

SECRET_KEY = 'django-insecure-u(&j6yyf8llzbv))6!17t$+bb9h8jnyz0s7s%n))k!4juk&5hs'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '20.119.97.89']
if 'CODESPACE_NAME' in os.environ:
    ALLOWED_HOSTS.append(f'{os.environ["CODESPACE_NAME"]}-8000.app.github.dev')
ALLOWED_HOSTS.append('*')  # Libera geral (ajuste para produção)
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

DATE_FORMAT = 'd/m/Y'

# Aplicações instaladas
INSTALLED_APPS = [
    'rest_framework',
    'nanny_pets_app',
    'django_filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'drf_yasg',
    'rest_framework.authtoken',
]

# DRF config
# ...

# DRF config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # 🔒 Protege a API por padrão
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.openapi.AutoSchema',
}

# 🔓 Libera o Swagger sem autenticação (isso afeta apenas a interface do Swagger, não a API em si)
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': None,
}

# Se quiser liberar só no modo DEBUG (ambiente local)
if DEBUG:
    REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = [
        'rest_framework.permissions.AllowAny'
    ]


# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://20.119.97.89:8000",
    "https://nannyspets-be-drc8ggc3d4c7hxfr.brazilsouth-01.azurewebsites.net",
]
CORS_ALLOW_ALL_ORIGINS = True

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

# DATABASES (dinâmico entre SQLite local e PostgreSQL prod)
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

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos e de mídia
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Campo padrão para primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'