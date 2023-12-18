FROM python:3.9-alpine
LABEL maintainer = "HD 43703"
WORKDIR /usr/src
RUN apk add --update --no-cache \
    g++ \
    gcc \
    build-base \
    jpeg-dev \
    zlib-dev \
    libpq-dev \
    python3-dev


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

#FROM python:3.9-alpine
#
#ENV PYTHONUNBUFFERED 1
#ENV PYTHONDONTWRITEBYTECODE 1
#
#WORKDIR /app/backend
#
#COPY requirements.txt /app/backend/
#
## Build psycopg2-binary from source -- add required required dependencies
#RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc python3-dev musl-dev && \
#        pip install --no-cache-dir -r requirements.txt && \
#        apk --purge del .build-deps
#
#COPY . /app/backend/
#
#CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]