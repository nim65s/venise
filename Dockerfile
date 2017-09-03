FROM python:latest

ADD requirements.txt /
RUN pip install -r /requirements.txt
ADD transhumus /transhumus

ENV PYTHONUNBUFFERED 1
