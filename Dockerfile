FROM debian:stable

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install git python python-dev python-pip -y
RUN apt-get install freetds-dev -y
RUN git clone https://github.com/e7217/sample
RUN pip install pymssql serial

RUN mv sample/fp ./agent