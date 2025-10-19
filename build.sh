#!/usr/bin/env bash
# build.sh

# 1. Instala dependências
pip install -r requirements.txt

# 2. Roda a migração no banco de dados limpo
python manage.py migrate

# 3. Coleta arquivos estáticos
python manage.py collectstatic --noinput