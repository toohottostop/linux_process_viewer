#!/usr/bin/env bash
if [[ "$1" = "start" ]]; then
  echo "Start client and server"
  python ps_viewer/manage.py runserver 1> logs/django_log.log 2> logs/django_errors.log &
  sleep 2
  python daemon_client.py
elif [[ "$1" = "stop" ]]; then
    echo "Stop client and server"
    CLIENT_PID=$(pidof -s python daemon_client.py)
    kill -9 "$CLIENT_PID"
    DJANGO_SERVER_PID=$(pidof -s python ps_viewer/manage.py runserver)
    kill -9 "$DJANGO_SERVER_PID"
fi