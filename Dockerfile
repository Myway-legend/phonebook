FROM python:3.9

MAINTAINER Konstantin Samoilenko

RUN apt-get update

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV FLASK_ENV="docker"

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["start.py"]