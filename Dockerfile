FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/dastan:$PYTHONPATH

WORKDIR /app

COPY ./requirements/dev.txt /app

RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r dev.txt

COPY . /app

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "core.wsgi:application"]
