FROM python:3.6

RUN pip install cassandra-driver

ADD initCassandra.py /

WORKDIR /

CMD python initCassandra.py
