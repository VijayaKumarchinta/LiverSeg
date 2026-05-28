FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/
RUN chmod +x /app/start.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Create directory for media files
RUN mkdir -p /app/media/ct_scans /app/media/liver_masks /app/media/preview_images

EXPOSE 8000

CMD ["/app/start.sh"]
