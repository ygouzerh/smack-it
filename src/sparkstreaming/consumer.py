from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":

    sc = SparkContext(appName="PythonStreamingKafkaWordCount")
    ssc = StreamingContext(sc, 10)

    kvs = KafkaUtils.createStream(ssc, "localhost:2181", "test-consumer-group", {"france": 5})
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.replace('"',"").replace("'","").split("\\")) \
        .map(lambda word: (word, 1)) \
        .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
