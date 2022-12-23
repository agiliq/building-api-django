FROM python:3.9.0

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

ENTRYPOINT ["python3", "manage.py"]

CMD ["runserver", "0.0.0.0:8800"]

