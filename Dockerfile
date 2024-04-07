# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

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

# Run alembic upgrade head before starting the Python application
CMD ["alembic", "upgrade", "head"]

# Start the Python application
CMD ["python", "main.py"]