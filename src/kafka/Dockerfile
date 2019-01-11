FROM ubuntu:trusty


RUN apt-get update && apt-get install -yq python3-pip && apt-get clean && rm -rf /var/lib/apt/lists
RUN pip3 install kafka-python tweepy emoji

ADD random_producer.py /

ENTRYPOINT [ "python3", "random_producer.py"]
