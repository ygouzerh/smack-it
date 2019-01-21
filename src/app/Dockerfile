FROM python:alpine3.6


RUN pip3 install cassandra-driver==3.16.0
RUN pip3 install flask flask_googlemaps
RUN pip3 install -U flask_cors


ADD style.css /
COPY templates/ /templates/
ADD cassandraFlask.py /



ENTRYPOINT [ "python3", "cassandraFlask.py"]
