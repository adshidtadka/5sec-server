FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3 python3-pip -y

RUN mkdir /app
COPY . /app

RUN pip3 install -r /app/requirements.txt

EXPOSE 5000

CMD cd /app && python3 5sec-server.py
