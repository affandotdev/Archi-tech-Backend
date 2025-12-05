#!/bin/sh

echo "Waiting for Postgres..."

while ! nc -z auth_db 5432; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up!"

python auth_service/manage.py migrate
python auth_service/manage.py runserver 0.0.0.0:8000
 