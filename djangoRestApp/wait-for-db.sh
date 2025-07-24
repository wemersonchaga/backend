#!/bin/sh

# Uso: ./wait-for-db.sh <host> <port>

host="$1"
port="$2"

echo "⏳ Aguardando o banco de dados em $host:$port..."

while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "✅ Banco de dados disponível em $host:$port"
