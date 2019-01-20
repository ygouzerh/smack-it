FROM python:alpine3.6
RUN pip install cassandra-driver==3.16.0

ADD create_tables.py /

# ADD display.py /

CMD ["python3", "create_tables.py"]
