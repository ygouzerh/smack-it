from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import listOfEmojis
#Variables that contains yours credentials to access Twitter API
access_token = "1971815509-Nqhhs9Kk9BW8IDXcdGWRKVA23HpAIjvsFbKFNpv"
access_token_secret =  "Kzst7eHw8hBakWmgGZyQnQaCwJYs22XwGSUOzdmJyFRjn"
consumer_key =  "iafm6Of1QyKFox3nGFIMJOiTi"
consumer_secret =  "y7Yi62gwQMm9a5rYw8j1avZNDyze9oAYNwC8udbXqBPCcljSD5"

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_status(self, status):
        if status.place:
            print(status.text)
            print(status.place.country)
            with open('tweets.json','a+') as outfile:
                json.dump(status._json, outfile)
                outfile.write("\n")

    def on_error(self, status):
        print(status)
        if status == 420:
            print("Rate limit reached. Disconnecting.")#returning False in on_data disconnects the stream
            return False

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    emojiList = []
    for emoji in listOfEmojis.veryPositive+listOfEmojis.positive+listOfEmojis.negative+listOfEmojis.veryNegative:
        emojiList.append(chr(int(emoji, 16)))
    # stream.filter(track=["France","football","sport","soccer","basket","happy","sad","emoji","a","i","the", "to", "of", "and", "e", "o", "y", "la", "un", "hello", "chocolate", "Coca-Cola", "louse", "google", "twitter"])
    stream.filter(track=emojiList)


# id pays id_emoji nb_occurence date
