# core/settings.py

# --- NOVAS IMPORTAÇÕES DE PRODUÇÃO (CRÍTICAS) ---
import os
from pathlib import Path
from decouple import config
# Importamos dj_database_url aqui apenas para garantir que o Render o encontre no bloco DATABASES
# (Apesar do erro anterior, ele precisa ser importado)
import dj_database_url 


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURANÇA (Puxando do .env)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-ldgz(x=n=t69-@k^336y=uv)a2k*hfsi!k+mq7qklqjphl=bcb')

# DEBUG: Puxa do .env (True para local, False para produção)
DEBUG = config('DEBUG', default=True, cast=bool)

# PERMISSÕES DE HOSTS (Puxa do .env e separa por vírgula. Default='*' para evitar quebra)
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
    'whitenoise.middleware.WhiteNoiseMiddleware', 

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


# Database (Lógica que Prioriza a Variável de Ambiente do Render)
# O Render fornece a URL completa via DATABASE_URL
if config('DATABASE_URL', default=None):
    # Se a variável DATABASE_URL estiver presente (ambiente de produção/Render)
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,  # Conexão persistente
            ssl_require=True   # Força SSL (necessário no Render)
        )
    }
else:
    # Fallback para desenvolvimento local usando os valores do .env local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='autovalue_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='autovalue2025'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5433'),
            # Opções de conexão local, se for o caso:
            'CONN_MAX_AGE': 600,
            'OPTIONS': {} 
        }
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
    "http://localhost:5173", 
    "http://127.0.0.1:5173", 
    "https://autovalue-frontend.vercel.app", # Domínio em Produção
]