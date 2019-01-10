
from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


countries = ["france"]


if __name__ == "__main__":

    sc = SparkContext(appName="TweetesProcessing")
    ssc = StreamingContext(sc, 10)

    # decodes the key-value kafka message using utf-8 decoder
    kvs = KafkaUtils.createStream(ssc, "kafka-zookeeper:2181", "test-consumer-group", {"emojis": 1})

    # will create receivers and consume the Kafka topics
    # explication for c:1 : https://stackoverflow.com/questions/48161253/what-is-the-correct-way-to-use-the-topics-parameter-in-kafkautils-createstream
    # and https://spark.apache.org/docs/1.6.1/streaming-kafka-integration.html (points to remember)
    #kafkaStreams = [KafkaUtils.createStream(ssc, "kafka-zookeeper:2181", {c:1}) for c in countries]
    #kvs = streamingContext.union(*kafkaStreams)

    # Just one topic: tweets
    # get (country, emojies)
    # lines = kvs.map(lambda m: (m[0], m[1]))

    #lines = kvs.map(lambda x: x[1])
    # counts = lines.flatMap(lambda line: line.replace('"',"").replace("'","").split(",")) \
    #counts = lines.flatMap(lambda line: line.split(",")) \
    counts = kvs.flatMap(lambda m: (m[0], m[1].split(","))) \
        .map(lambda (c, emo): (c, (, ))) \
        .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
