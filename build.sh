#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "from django.db import connection; print('DATABASE_BACKEND:', connection.vendor)"
