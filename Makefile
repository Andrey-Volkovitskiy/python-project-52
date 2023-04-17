MANAGE := poetry run python3 manage.py

install:
	poetry install

start:
	poetry run gunicorn task_manager.wsgi

railway-start:
	python manage.py migrate && gunicorn task_manager.wsgi

dev:
	$(MANAGE) runserver

dev-eng:
	env LANGUAGE_CODE='en-us' $(MANAGE) runserver

db-container:
	docker compose up -d

createsuperuser:
	python manage.py createsuperuser

lint:
	poetry run flake8 task_manager

test:
	env poetry run python3 -m pytest -ra -s -vvv tests/

cov:
	poetry run python3 -m pytest --cov=task_manager/ tests/

translate-to-ru:
	django-admin makemessages -l ru

re-translate:
	django-admin makemessages -a

compile-msg:
	django-admin compilemessages

migrate:
	poetry run python3 manage.py migrate