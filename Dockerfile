FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install

RUN apt-get update \
    && apt-get -y install build-essential libpq-dev \
    && apt-get clean

RUN python -m pip install --upgrade pip

WORKDIR /code
COPY requirements/prod.txt /code/
RUN pip install -r prod.txt
COPY . /code/
