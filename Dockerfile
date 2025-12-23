FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create a non-root user for security
RUN useradd -m django-user
USER django-user

COPY . /app/

EXPOSE 8000

# Fix: Added missing comma between arguments
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]