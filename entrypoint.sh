#!/bin/bash
# Copy the .env file to the /app directory
if [ -f "/env/.env" ]; then
  cp /env/.env /app/.env
  echo ".env file copied to /app directory."
else
  echo ".env file not found in /env directory."
fi

cd /app

if [ -f "/app/.env" ]; then
  set -o allexport
  source /app/.env
  set +o allexport
fi

if [ -z "$CRON_EXPRESSION" ]; then
  echo "CRON_EXPRESSION is not set. Exiting."
  exit 1
fi

echo "$CRON_EXPRESSION /usr/local/bin/python3 /app/main.py >> /app/cron.log 2>&1" > /etc/cron.d/app-cron
chmod 0644 /etc/cron.d/app-cron
crontab /etc/cron.d/app-cron

touch /var/log/cron.log /app/cron.log

service cron start

echo "Cron started with expression: $CRON_EXPRESSION"

tail -f /var/log/cron.log /app/cron.log



