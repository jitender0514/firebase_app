# Pull base image
FROM python:3.10.8

# Set the file maintainer
LABEL maintainer="jitender singh <jitender0514@gmail.com>"

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# System dependencies.
RUN apt-get update && apt-get install -y wait-for-it vim man jq awscli nginx \
    certbot cron

# Python dependencies.
COPY requirements.txt /opt/requirements.txt
RUN pip install -U pip && pip install -r /opt/requirements.txt

# Port to expose
EXPOSE 8000

# Set work directory
WORKDIR /app

# Entrypoint
COPY docker-entrypoint.sh /usr/bin/
ENTRYPOINT ["docker-entrypoint.sh"]

# Copy project
COPY . /app
#COPY letsencrypt /etc/letsencrypt
#
## Download ssl certifate
#RUN wget -O /etc/letsencrypt/archive/api.bramework.com/fullchain1.pem \
#    https://bramework-ssl-cert.s3.amazonaws.com/api.bramework.com/fullchain.pem
#RUN wget -O /etc/letsencrypt/archive/api.bramework.com/privkey1.pem \
#    https://bramework-ssl-cert.s3.amazonaws.com/api.bramework.com/privkey.pem

ARG ENV
RUN if [ "$ENV" = "local" ]; then cp nginx/nginx.conf \
    /etc/nginx/sites-available/default; fi
RUN if [ "$ENV" = "dev" ]; then cp nginx/nginx-dev.conf \
    /etc/nginx/sites-available/default; fi
RUN if [ "$ENV" = "prod" ]; then cp nginx/nginx-prod.conf \
    /etc/nginx/sites-available/default; fi

# Build and copy static files
#RUN if [ "$ENV" != "dev" ] && [ "$ENV" != "beta" ]; then \
#    SECRET_KEY=secret python manage.py collectstatic --noinput; \
#    cp -r /app/staticfiles /var/www/html/static; fi
#
## Added cron job
#RUN echo '*/5 * * * * . /app/local.env;python /app/manage.py runcrons \
#    > /app/cronjob.log' > /etc/cron.d/runcrons
#RUN crontab /etc/cron.d/runcrons

CMD [ "gunicorn", "firebaseProject.wsgi:application", \
    "--bind", "0.0.0.0:8000", \
    "--worker-class=gevent", \
    "--workers", "3", \
    "--timeout", "300", \
    "--enable-stdio-inheritance" ]
