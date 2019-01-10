

from kafka import KafkaProducer
import json
import time
import emoji

emojies = [😀, 😭, 🤖, 😡, 🥶]

tweets = ["Je suis 😀😀blabla", "Ana 😭😭😭blabla", "Ich bin 🤖blabla", "I'm 😡😡😡😡blabla", "Я 🥶blabla"]
countries = ["france", "morocco", "germany", "usa", "russia"]


def extract_emojis(tweet):
    return ','.join(c for c in tweet if c in emoji.UNICODE_EMOJI)



producer = KafkaProducer(bootstrap_servers=['kafka:9092'])

while 1:

    print(extract_emojis(chosen_tweet).encode('utf-8'))
    print(extract_emojis(chosen_tweet).encode('utf-8').decode('utf-8'))

    for i, c in enumerate(countries) :
        # send (country, emojies) to kafka brokers
        producer.send('emojis', key=c, value=extract_emojis(tweets[i]).encode('utf-8'))

    #print(json.dumps(extract_emojis(chosen_tweet)).encode('utf-8'))


    time.sleep(0.1)
