# core/settings.py

# --- NOVAS IMPORTAÇÕES DE PRODUÇÃO (CRÍTICAS) ---
import os
import dj_database_url
from decouple import config
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production

# SEGURANÇA (Puxando do .env)
SECRET_KEY = config('SECRET_KEY')

# DEBUG: Puxa do .env (True para local, False para produção)
DEBUG = config('DEBUG', default=True, cast=bool)

# PERMISSÕES DE HOSTS (Puxa do .env e separa por vírgula)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',') 


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Nossos Apps
    'corsheaders',
    'rest_framework',
    'veiculos',
]

MIDDLEWARE = [
    # Middlewares de Produção (WhiteNoise e CORS no topo)
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Para servir arquivos estáticos em produção

    # Middlewares Padrão
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database (Lê a URL de conexão completa do Render)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,  # Adiciona persistência da conexão
        ssl_require=True   # Força o uso de SSL/TLS (necessário no Render)
    )
}


# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CRUCIAL PARA WHITENOISE EM PRODUÇÃO)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração CORS (Permite comunicação com o React em ambiente de desenvolvimento e produção)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # Desenvolvimento local
    "http://127.0.0.1:5173", # Desenvolvimento local
    "https://autovalue-frontend.vercel.app", # <--- ADICIONE ESTA LINHA!
    # Aqui entrará o domínio público do seu frontend (Vercel/Netlify)
]