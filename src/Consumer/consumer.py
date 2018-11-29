from kafka import KafkaConsumer
import json
from cassandra.cluster import Cluster

address = 'localhost'

cluster = Cluster([address])
session = cluster.connect("emoji")

consumer = KafkaConsumer('France', bootstrap_servers=['localhost:9092'])

for message in consumer:

    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
    session.execute("INSERT INTO pays (nom_pays, emojis) VALUES ("+message.topic+", ['"+message.value+"']);")
