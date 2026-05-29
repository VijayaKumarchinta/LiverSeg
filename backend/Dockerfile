FROM python:3.12-slim

# ─────────────────────────────────────────────
# ENVIRONMENT
# ─────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TMPDIR=/var/tmp
WORKDIR /app

# ─────────────────────────────────────────────
# SYSTEM DEPENDENCIES
# ─────────────────────────────────────────────
RUN apt-get update && apt-get install -y gcc libpq-dev curl libmagic1 && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────
# PYTHON DEPENDENCIES
# ─────────────────────────────────────────────
COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# ─────────────────────────────────────────────
# COPY PROJECT
# ─────────────────────────────────────────────
COPY . .

# ─────────────────────────────────────────────
# MEDIA + STATIC DIRECTORIES
# ─────────────────────────────────────────────
RUN mkdir -p \
    /app/media/ct_scans \
    /app/media/liver_masks \
    /app/media/preview_images \
    /app/staticfiles \
    /var/log/liverseg

# ─────────────────────────────────────────────
# CREATE NON-ROOT USER
# ─────────────────────────────────────────────
RUN adduser --disabled-password --gecos "" appuser

RUN chown -R appuser:appuser /app

RUN chown -R appuser:appuser /var/log/liverseg

USER appuser

# ─────────────────────────────────────────────
# START SCRIPT
# ─────────────────────────────────────────────
RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]