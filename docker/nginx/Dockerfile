FROM --platform=linux/amd64 python:3.10.2-buster AS django-static-builder
WORKDIR /code
COPY . .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y netcat
RUN pip install --upgrade pip

RUN pip install -r ./requirements.txt

RUN python manage.py collectstatic --no-input


FROM --platform=linux/amd64 nginx:1.21 AS front

COPY --from=django-static-builder /code/static /code/static/

COPY ./docker/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/nginx/conf.d /etc/nginx/conf.d

