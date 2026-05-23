FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Alpine uses apk instead of apt-get
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libpq-dev \
    curl \
    build-base

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "bookrental.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3"]