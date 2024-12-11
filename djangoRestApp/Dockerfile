# Para obter mais informações, consulte https://aka.ms/vscode-docker-python
#FROM python:3.9
# Use Python 3.10 como imagem base
FROM python:3.10

EXPOSE 8000
# Desativa o buffer para facilitar o registro do contêiner
ENV PYTHONUNBUFFERED=1

#Define o diretório de trabalho
WORKDIR /djangoRestApp

# Copie requisitos.txt primeiro para fins de armazenamento em cache
COPY requirements.txt .

# Instale os requisitos do pip
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copie o restante do código da sua aplicação
COPY . .

# Durante a depuração, este ponto de entrada será substituído. Para obter mais informações, consulte https://aka.ms/vscode-docker-python-debug
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]