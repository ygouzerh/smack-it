# from geopy.geocoders import Yandex
# import json
# geolocator = Yandex(lang='en_US')
#
# location = geolocator.geocode("Paris", timeout=10)
#
# if location != None:
#     print (json.dumps(location.raw, indent=4))
#     print (location.address)
#     print (location.latitude, " -> ", location.longitude)
# else:
#     print (location)

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

access_token = "1971815509-Nqhhs9Kk9BW8IDXcdGWRKVA23HpAIjvsFbKFNpv"
access_token_secret =  "Kzst7eHw8hBakWmgGZyQnQaCwJYs22XwGSUOzdmJyFRjn"
consumer_key =  "iafm6Of1QyKFox3nGFIMJOiTi"
consumer_secret =  "y7Yi62gwQMm9a5rYw8j1avZNDyze9oAYNwC8udbXqBPCcljSD5"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth)
places = api.geo_search(query="FR", granularity="country")
place_id = places[0].id
tweets = api.search(q="place:%s" % place_id)
for tweet in tweets:
    print(tweet[0].text)
