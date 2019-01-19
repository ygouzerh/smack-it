import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from cassandra.cluster import Cluster

def traitement(rdd):
    rdd.foreach(lambda record: sendCassandra(record))

def sendCassandra(record):
    cs_cluster = Cluster(['cassandra-db'])
    cs_session = cs_cluster.connect("emoji")
    cs_session.execute("INSERT INTO EMOJI_PACKAGE (id, pays, id_emoji, nb_occurence, package_date) VALUES (now(),%s,%s,%s,toTimestamp(now())) ",[record[0],record[1],record[2]])



if __name__ == "__main__":

    sc = SparkContext(appName="SMACKIT")
    ssc = StreamingContext(sc, 10)

    kvs = KafkaUtils.createStream(ssc, "kafka-zookeeper:2181", "test-consumer-group", {"emojis": 1})
    counts = kvs.flatMap(lambda m: [(m[0], em) for em in  m[1].split(",")]) \
        .map(lambda m: (m, 1)) \
        .reduceByKey(lambda a, b: a+b) \
        .map(lambda m: (m[0][0], m[0][1], m[1])) \
        .foreachRDD(traitement)


    ssc.start()
    ssc.awaitTermination()

    #cs_session.shutdown();
    #cs_cluster.shutdown();
