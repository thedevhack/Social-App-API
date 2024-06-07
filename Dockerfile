
FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR ls

COPY ./app/ .

RUN pip install -r requirements.txt

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput
