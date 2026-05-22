# ── Base image ─────────────────────────────
FROM docker.io/library/python:3.11-slim

# ── Environment ─────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SECRET_KEY=change-me-in-production \
    PIP_NO_CACHE_DIR=1

# ── Working directory ───────────────────────
WORKDIR /app

# ── Install system dependencies ─────────────
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        curl \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

# ── Install Python dependencies ─────────────
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Copy project ────────────────────────────
COPY . .

# ── Django setup ────────────────────────────
RUN python manage.py collectstatic --noinput || true

# ── Expose port ─────────────────────────────
EXPOSE 8000

# ── Start server ────────────────────────────
CMD ["gunicorn", "bookrental.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
