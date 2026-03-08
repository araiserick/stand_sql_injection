FROM python:3.11.4-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src src
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Создаём директорию для БД
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["bash", "entrypoint.sh"]