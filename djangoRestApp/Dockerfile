# Para obter mais informações, consulte https://aka.ms/vscode-docker-python
FROM python:3.9

EXPOSE 8000

# Desativa o buffer para facilitar o registro do contêiner
ENV PYTHONUNBUFFERED=1


WORKDIR /nanny_pets
COPY . /nanny_pets
# Instale os requisitos do pip
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Durante a depuração, este ponto de entrada será substituído. Para obter mais informações, consulte https://aka.ms/vscode-docker-python-debug
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]