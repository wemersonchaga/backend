FROM python:3.10

EXPOSE 8000
ENV PYTHONUNBUFFERED=1

WORKDIR /djangoRestApp

COPY requirements.txt .

RUN apt-get update && apt-get install -y netcat-openbsd && \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

COPY . .

RUN chmod +x wait-for-db.sh

CMD ["sh", "-c", "./wait-for-db.sh db 5432 && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
