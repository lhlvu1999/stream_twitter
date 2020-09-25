from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from stream_tweets import twitter_credentials, transports
from streaming import kafka_streaming


# # # TWITTER AUTHENTICATOR # # #
class TwitterAuthenticator:

    @staticmethod
    def authenticator_twitter_app():
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                            twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                              twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


# # # TWITTER STREAMER # # #
class TwitterStreamer:
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.producer = kafka_streaming.producer
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, hash_tag_lists):
        # This is handles Twitter authentication
        # and the connection to the Twitter Streaming API.
        listener = TwitterListener(self.producer)

        auth = self.twitter_authenticator.authenticator_twitter_app()

        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_lists)


# # # TWITTER STREAM LISTENER # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener class that just prints received tweets to stdout
    """
    def __init__(self, producer):
        self.producer = producer

    def on_data(self, raw_data):
        try:
            # # # STEP transport data to DB and to Kafka # # #
            transports.stream(raw_data, self.producer)
        except BaseException as e:
            print("Error on_data %s" % str(e))

        return True

    def on_error(self, status_code):
        print(status_code)
