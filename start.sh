venv/bin/gunicorn --access-logfile - --workers 3 --bind 0.0.0.0:8007 intelli-pos.wsgi:application
