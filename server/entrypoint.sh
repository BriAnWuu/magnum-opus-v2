#!/bin/sh

# Run migrations and collect static (optional)
python manage.py migrate --noinput
# python manage.py collectstatic --noinput

# Start server
# exec gunicorn server.wsgi:application --bind 0.0.0.0:${PORT:-8000}
exec daphne -b 0.0.0.0 -p 8000 server.asgi:application