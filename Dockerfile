# ── Base image ──────────────────────────────────────────────
FROM python:3.11-slim

# ── Environment variables ────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SECRET_KEY=change-me-in-production

# ── Working directory inside container ──────────────────────
WORKDIR /app

# ── Install system dependencies ──────────────────────────────
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ── Install Python dependencies ──────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ── Copy the entire project ──────────────────────────────────
COPY . .

# ── Collect static files ─────────────────────────────────────
RUN python manage.py collectstatic --noinput

# ── Expose port ──────────────────────────────────────────────
EXPOSE 8000

# ── Start Gunicorn ───────────────────────────────────────────
# bookrental = folder containing settings.py = your Django config module
CMD ["gunicorn", "bookrental.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]