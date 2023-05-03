FROM python:3.8

# Define work dir
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean && apt-get install -y vim

RUN pip install --upgrade pip
# Copy reqs
COPY ./requirements.txt .
# Install reqs
RUN pip install -r requirements.txt


# Copy all stuff
COPY . /app
