import socket
import time
import os

host = os.environ.get("DB_HOST", "localhost")
port = int(os.environ.get("DB_PORT", 5432))

print(f"⏳ Aguardando o banco de dados em {host}:{port}...")

while True:
    try:
        with socket.create_connection((host, port), timeout=1):
            print("✅ Banco de dados disponível!")
            break
    except OSError:
        time.sleep(1)
