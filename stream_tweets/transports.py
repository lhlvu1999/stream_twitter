from helper.modify import Modify
from database.dml import query
from database.dml.database import SessionLocal


class Transports:
    def __init__(self, raw_data):
        self.data = Modify(raw_data)

    def insert_into_db(self):
        data = self.data
        db = SessionLocal()

        # insert subject table
        subject = query.SubjectRepository(db)
        subject_value = data.get_subject()
        check_subject = subject.get_subject(subject_value)
        if not check_subject:
            subject.insert_subject(subject_value)

        # insert date table
        date = query.DateRepository(db)
        date_id, month, day, year, hour, minus, period, day_in_week = data.get_date_user()
        date_user = date.get_date(date_id)

        if not date_user:
            date.insert_date(date_id, month, day, year, hour, minus, period, day_in_week)

        date_id, month, day, year, hour, minus, period, day_in_week = data.get_date_tweet()
        date_tweet = date.get_date(date_id)
        if not date_tweet:
            date.insert_date(date_id, month, day, year, hour, minus, period, day_in_week)

        # insert User table
        user = query.UserRepository(db)
        user_id, name, screen_name, description, followers_count, \
        friends_count, status_count, lang, date_id = data.get_user()
        check_user = user.get_user(user_id)
        if not check_user:
            user.insert_user(user_id, name, screen_name, description, followers_count,
                              friends_count, status_count, lang, date_id)

        # insert Fact_tweet table
        tweet = query.TweetRepository(db)
        tweet_id, user_id, subject_id, date_id, text, source, lang = data.get_tweet()
        subject_name = data.get_subject()
        subject_id = subject.get_subject_id(subject_name)
        tweet.insert_fact_tweet(tweet_id, user_id, subject_id, date_id, text, source, lang)

        db.close()
        print("Insert to db success")

    def producer_kafka(self, topic, producer):
        data = self.data
        tweet_id = data.get_attribute('tweet_id')
        user_id = data.get_attribute('user_id')
        source = data.get_attribute('source')
        text = data.get_attribute('text')
        date_tweet = data.get_attribute('date_tweet')
        lang = data.get_attribute('lang_tweet')
        test_data = {
            'tweet_id': tweet_id,
            'user_id': user_id,
            'source': source,
            'text': text,
            'created_at': date_tweet,
            'lang': lang
        }
        producer.send(topic=topic, value=test_data)
        # print(test_data)
        # print('-----')
        print(f"Success produce to {topic} kafka")


def stream(raw_data, producer):
    data = Transports(raw_data)
    data.insert_into_db()
    data.producer_kafka(topic='numtest', producer=producer)
