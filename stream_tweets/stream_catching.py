from stream_tweets.catching_tweet import TwitterStreamer
from helper.variable import sports


if __name__ == "__main__":
    tweet_live = TwitterStreamer()
    tweet_live.stream_tweets(hash_tag_lists=sports)
