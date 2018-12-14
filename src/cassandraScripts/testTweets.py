from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

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
        print(status.text)

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['happy'])
