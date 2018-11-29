FROM python:3.6

RUN pip install kafka-python
RUN pip install cassandra-driver

ADD select.py /

WORKDIR /

#CMD python -c 'import cassandra; print(cassandra.__version__)'
CMD python select.py
