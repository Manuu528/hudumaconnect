#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "from django.db import connection; print('DATABASE_BACKEND:', connection.vendor)"

if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && \
   [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && \
   [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
    python manage.py createsuperuser --noinput || \
        echo "Superuser already exists or creation needs checking."
fi
