venv/bin/gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:8007 --log-config gunicorn.conf intelli-pos.wsgi:application 