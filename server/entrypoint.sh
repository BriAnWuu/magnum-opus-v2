#!/bin/sh

# Wait for PostgreSQL to be ready
echo "Waiting for postgres..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Wait for Redis to be ready (optional, but good practice for Channels)
echo "Waiting for redis..."
while ! nc -z redis 6379; do
  sleep 0.1
done
echo "Redis started"

# Run migrations and collect static (optional)
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start server
# exec gunicorn server.wsgi:application --bind 0.0.0.0:${PORT:-8000}
echo "Starting Django application with Daphne..."
exec daphne -b 0.0.0.0 -p 8000 server.asgi:application
