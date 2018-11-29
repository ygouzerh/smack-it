# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer

import json
import emoji

#Variables that contains yours credentials to access Twitter API
access_token = ""
access_token_secret =  ""
consumer_key =  ""
consumer_secret =  ""

GEOBOX_GERMANY = [5.0770049095, 47.2982950435, 15.0403900146, 54.9039819757]
country="Germany"

#listner pour afficher les composants essentiels des tweets en sortie std
class StdOutListener(StreamListener):

    def on_data(self, data):
        doc=json.loads(data)
        print(doc['text'])
        print("---")
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda v: json.dumps(v).encode('utf-8'))

        future=producer.send('kafkatopic', "Country "+country+" Emojis "+self.extract_emojis(doc['text']))

        producer.flush()

    def on_error(self, status):
        print(status)

    def extract_emojis(self, str):
        return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)

if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l, tweet_mode='extended')

    stream.filter(locations=GEOBOX_GERMANY)
