# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install required utilities
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry==1.8.0

# Set the working directory in the container
WORKDIR /app

# Copy the dependency files
COPY pyproject.toml poetry.lock /app/

# Generate requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . /app/

# Download and install wait-for-it
RUN curl -s https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh > /usr/bin/wait-for-it \
    && chmod +x /usr/bin/wait-for-it

# Run alembic upgrade head after waiting for the PostgreSQL service to be available
CMD ["sh", "-c", "wait-for-it postgres_db:5432 --timeout=30 --strict -- alembic upgrade head && python main.py"]