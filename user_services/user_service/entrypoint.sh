#!/bin/sh

echo "Waiting for Postgres..."

until python3 - <<END
import psycopg2, os
try:
    psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    print("OK")
except:
    exit(1)
END
do
  echo "Postgres unavailable - sleeping"
  sleep 2
done

echo "Postgres is up!"
echo "Running migrations..."
python manage.py migrate

echo "Starting RabbitMQ consumer…"
python - << 'EOF' &
from infrastructure.message_broker import start_user_created_consumer
start_user_created_consumer()
EOF

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT
