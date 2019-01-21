from kafka import KafkaProducer
import json
import time
import emoji
from random import choice

tweets = ["😀","😀","😀","😀","😀","😡","😡","😡","😡","😡"]
countries = ["France", "Espagne", "Maroc", "Canada", "USA", "Algerie", "Japon", "Russie", "AfriqueDuSud", "Allemagne"]



producer = KafkaProducer(bootstrap_servers=['kafka:9092'])



def extract_emojis(tweet):
    return ','.join(c for c in tweet if c in emoji.UNICODE_EMOJI)


while 1:

    producer.send('emojis', key=choice(countries).encode('utf-8'), value=extract_emojis(choice(tweets)).encode('utf-8'))


    time.sleep(0.001)
