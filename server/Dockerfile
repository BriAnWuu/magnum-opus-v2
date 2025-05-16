# Stage 1: Build stage
FROM python:3.13-slim

# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Set an environment variable to unbuffer Python output, aiding in logging and debugging
ENV PYTHONBUFFERED=1

# Set the working directory within the container to /app for any subsequent commands
WORKDIR /app

# Upgrade pip to ensure we have the latest version for installing dependencies
RUN pip install --upgrade pip

# Copy the entire current directory contents into the container at /app
COPY requirements.txt /app/

# Install dependencies from the requirements.txt file to ensure our Python environment is ready
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Entrypoint script as the container command
# CMD ["./entrypoint.sh"]

# For production with Daphne (if using Django Channels)
# CMD ["daphne", "server.asgi:application", "--bind", "0.0.0.0", "--port", "8000"]