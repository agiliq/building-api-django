FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

# Copying & Installing python requirements
COPY ./pollsapi/requirements.txt /app/
RUN pip install -r requirements.txt

# Syncing the source of the application
COPY ./pollsapi/ /app/

EXPOSE 8000

# CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "pollsapi.wsgi:application" ]