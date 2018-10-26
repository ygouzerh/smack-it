import time
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Our filter function:
def filter_tweets(tweet):
    json_tweet = json.loads(tweet)
    if json_tweet.has_key('lang'): # When the lang key was not present it caused issues
        if json_tweet['lang'] == 'ar':
            return True # filter() requires a Boolean value
    return False

sc = SparkContext("local[2]", "Twitter Emojis")
ssc = StreamingContext(sc, 10) #10 is the batch interval in seconds
IP = "localhost"
Port = 9990
lines = ssc.socketTextStream(IP, Port)

# When your DStream in Spark receives data, it creates an RDD every batch interval.
# We use coalesce(1) to be sure that the final filtered RDD has only one partition,
# so that we have only one resulting part-00000 file in the directory.
# The method saveAsTextFile() should really be re-named saveInDirectory(),
# because that is the name of the directory in which the final part-00000 file is saved.
# We use time.time() to make sure there is always a newly created directory, otherwise
# it will throw an Exception.
lines.foreachRDD( lambda rdd: rdd.filter( filter_tweets ).coalesce(1).saveAsTextFile("./tweets/%f" % time.time()) )

ssc.start()
ssc.awaitTermination()
