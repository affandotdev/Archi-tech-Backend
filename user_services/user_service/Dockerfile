FROM python:3.10

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Install pika (RabbitMQ client)
RUN pip install pika

# Copy project code
COPY . .

# Expose port
EXPOSE 8001

# Entry point
CMD ["sh", "entrypoint.sh"]
# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd