FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./app ./app

RUN apt-get update
RUN apt-get -y install libspatialindex-dev

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
