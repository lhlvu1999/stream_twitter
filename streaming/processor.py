from nltk.tokenize import TweetTokenizer
from datetime import datetime
from helper.variable import sports
from helper.clean_data import convert_time_to_each10s
from streaming.events import Sports


def clean_data_from_tweet(tweets):
    football = 0
    all_sports = 0
    for tweet in tweets:
        sport = "Unknown"
        # split text to list of words
        words = TweetTokenizer().tokenize(tweet.text)
        for word in words:
            # get subject sport in text
            if word.lower() in sports:
                sport = word.lower()
                break
        if sport == 'football':
            football += 1
        all_sports += 1
    time = convert_time_to_each10s(datetime.utcnow())
    sports_in_period = Sports(time=time, football=football, all_sports=all_sports)
    print('Send to analyze:')
    return sports_in_period


def count_sports(event, football, sports):
    curr = convert_time_to_each10s(datetime.utcnow())
    # if current == time of event
    if curr == event.time:
        # update last 10 period time
        for i in range(9, 0, -1):
            football[i] = football[i - 1]
            sports[i] = sports[i - 1]
        football[0] = event.football
        sports[0] = event.all_sports
        print('a period = 10 seconds')
        print('last_10_period_football: ', football)
        print('last_10_period_sports: ', sports)
        print('___end___stage___')
    return [football, sports]
