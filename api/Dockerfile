# Pull base image
FROM python:3.7

WORKDIR /code

# Install dependencies
COPY /requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt \
    && rm /requirements.txt \
    && apt-get clean

COPY . .
