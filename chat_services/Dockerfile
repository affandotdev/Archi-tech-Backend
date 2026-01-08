FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat-openbsd \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies (assuming a requirements.txt exists or will be created)
# If not, we should generate one. For now, we'll try to copy one.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || echo "Requirements installation failed or file missing"

# Install daphne explicitly if not in requirements
RUN pip install daphne channels channels_redis psycopg2-binary django-cors-headers djangorestframework django stripe python-dotenv

COPY . .

# Expose port
EXPOSE 8002

# Run with Daphne for WebSocket support
CMD ["daphne", "-b", "0.0.0.0", "-p", "8002", "chat_services.asgi:application"]
