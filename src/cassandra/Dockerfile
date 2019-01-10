FROM python:alpine3.6
RUN pip install cassandra-driver==3.16.0
ADD create_tables.py /

ENTRYPOINT ["python3", "create_tables.py"]

