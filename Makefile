checkfiles = api/ billers/ config/ portal/ rates services/ transactions users/

run:
	python3 manage.py runserver

celery:
	celery -A config worker -l info

# celery-beat:
# 	celery -A config beat -l info 


superuser:
	python3 manage.py createsuperuser


migrations:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

style:
	black $(checkfiles)
