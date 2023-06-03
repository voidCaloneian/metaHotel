FROM python:latest

RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /meta

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./src ./src

