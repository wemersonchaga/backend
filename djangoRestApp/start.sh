#!/bin/bash

# Define host e porta do banco de dados
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}

echo "Esperando o banco de dados em $DB_HOST:$DB_PORT..."
python wait_for_db.py

echo "Rodando migrações..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
gunicorn tutorial.wsgi:application --bind 0.0.0.0:8000
