FROM python

EXPOSE 8000

RUN mkdir /app
WORKDIR /app

RUN apt-get update -qqy \
 && apt-get install -qqy \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

ADD Pipfile Pipfile.lock ./

RUN pip3 install --no-cache-dir -U pipenv \
 && pipenv install --system --deploy

ADD . .

CMD while ! nc -z postgres 5432; do sleep 1; done \
 && ./manage.py migrate \
 && ./manage.py collectstatic --no-input \
 && ./manage.py runserver 0.0.0.0:8000
