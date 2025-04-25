# Stage 1: Build stage
FROM python:3.13-slim as builder

# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Set an environment variable to unbuffer Python output, aiding in logging and debugging
ENV PYTHONBUFFERED=1

# Define an environment variable for the web service's port, commonly used in cloud services
ENV PORT=8000

# Set the working directory within the container to /app for any subsequent commands
WORKDIR /app

# Upgrade pip to ensure we have the latest version for installing dependencies
RUN pip install --upgrade pip

# Install system dependencies:
# libpq-dev: Required for psycopg2 (PostgreSQL adapter)
# gcc: Required for compiling some Python packages
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Copy the entire current directory contents into the container at /app
COPY requirements.txt /app/

# Install dependencies from the requirements.txt file to ensure our Python environment is ready
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files (if you have any)
RUN python manage.py collectstatic --noinput

# Run database migrations to ensure the database schema is up to date
RUN python manage.py migrate --noinput

# Set the command to run our web service using Gunicorn, binding it to 0.0.0.0 and the PORT environment variable
CMD ['gunicorn', 'server.wsgi:application', '--bind', '0.0.0.0', '--port', ${PORT}]

# Inform Docker that the container listens on the specified network port at runtime
EXPOSE ${PORT}

# For production with Daphne (if using Django Channels)
# CMD ["daphne", "server.asgi:application", "--bind", "0.0.0.0", "--port", "8000"]