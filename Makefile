django-migrate:
	python manage.py migrate

start:
	./manage.py runserver

admin:
	DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=123123 \
	DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
	python manage.py createsuperuser --name=Adminko --noinput || true


make-trans:
	django-admin makemessages -l ru -e py -i venv
compile-trans:
	django-admin compilemessages --exclude venv


build-gateway:
	docker --log-level=debug build --pull --file=docker/nginx/Dockerfile --tag=rozarioagro/swarm-gateway:0.1 docker/nginx
	docker push rozarioagro/swarm-gateway:0.1

build-api:
	docker --log-level=debug build --pull --file=docker/api/Dockerfile --tag=rozarioagro/swarm-django:0.1 .
	docker push rozarioagro/swarm-django:0.1

build-all: build-gateway build-api