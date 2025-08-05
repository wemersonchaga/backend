#!/bin/bash

# Recebe host e port do banco via variáveis de ambiente ou padrão
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}

echo "Esperando o banco de dados em $DB_HOST:$DB_PORT..."
./wait-for-db.sh "$DB_HOST" "$DB_PORT"

echo "Rodando migrações..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

echo "Iniciando Gunicorn..."
gunicorn tutorial.wsgi:application --bind 0.0.0.0:8000
