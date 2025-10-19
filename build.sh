#!/usr/bin/env bash
# build.sh

# Exit on error
set -o errexit

# 1. Instala dependências
pip install -r requirements.txt

# 2. Roda as migrações (CRÍTICO)
python manage.py migrate

# 3. Coleta arquivos estáticos
python manage.py collectstatic --noinput

# O servidor é iniciado pelo comando de Start do Render: gunicorn core.wsgi