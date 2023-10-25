FROM python:3.8-slim-buster

RUN apt-get update

RUN apt-get -y install default-libmysqlclient-dev

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV DB_USER=cmd_svc
ENV DB_PASSWORD=secret
ENV DB_ADDR=localhost:3306
ENV DB_DATABASE=cmd_store_db
ENV PORT=9090

EXPOSE 9090

ENV FLASK_APP=server.py

CMD [ "python3", "server.py"]