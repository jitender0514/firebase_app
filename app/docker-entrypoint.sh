#!/usr/bin/env bash
set -o errexit
set -o pipefail

#wait-for-it --strict --quiet --timeout=30 $DB_HOST:5432

# Apply latest database migrations
python manage.py migrate --noinput
# Collect static files
python manage.py collectstatic --noinput
# Start nginx
service nginx start
# Start cron
/usr/bin/env > /app/local.env
sed -i 's/^/export /;s/=/=\"/;s/$/\"/' /app/local.env
#cron

exec "$@"
