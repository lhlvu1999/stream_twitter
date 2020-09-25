from sqlalchemy.orm import Session
from database.dml import models


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, user_id: str):
        with self.session as session:
            return session.query(models.User).filter(models.User.id == user_id).first()

    def get_user_post_tweet(self, tweet_id: str):
        with self.session as session:
            return session.query(models.User).join(models.Fact_tweet).filter(
                models.User.id == models.Fact_tweet.user_id,
                models.Fact_tweet.tweet_id == tweet_id).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        with self.session as session:
            return session.query(models.User).offset(skip).limit(limit).all()

    def insert_user(self, user_id, name, screen_name, description, followers_count,
                    friends_count, status_count, language, date_created_id):
        # id, name, screen_name, description, followers_count, friends_count,
        # status_count, language, date_created_id = user_values
        session_user = models.User(id=user_id, name=name, screen_name=screen_name, description=description,
                                   followers_count=followers_count, friends_count=friends_count,
                                   status_count=status_count, language=language, date_created_id=date_created_id)
        with self.session as session:
            session.add(session_user)
            session.commit()
            return session_user


class TweetRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_tweets(self, skip: int = 0, limit: int = 100):
        with self.session as session:
            return session.query(models.Fact_tweet).offset(skip).limit(limit).all()

    def get_tweets_with_subject(self, subject: str, skip: int = 0, limit: int = 100):
        with self.session as session:
            return session.query(models.Fact_tweet).join(models.Subject).filter(
                models.Fact_tweet.subject_id == models.Subject.id,
                models.Subject.name == subject).offset(skip).limit(limit).all()

    def get_sentiment(self, skip: int = 0, limit: int = 100):
        with self.session as session:
            return session.query(models.Fact_tweet.sentiment).offset(skip).limit(limit).all()

    def get_text(self, skip: int = 0, limit: int = 100):
        with self.session as session:
            return session.query(models.Fact_tweet.tweet_id, models.Fact_tweet.text).offset(skip).limit(limit).all()

    def insert_fact_tweet(self, tweet_id, user_id, subject_id, date_tweet, text, source, lang):
        # tweet_id, user_id, subject_id, date_tweet, text, source, lang_tweet = fact_tweet_values
        session_fact_tweet = models.Fact_tweet(tweet_id=tweet_id, user_id=user_id, subject_id=subject_id,
                                               date_created_id=date_tweet, text=text, source=source, language=lang)
        with self.session as session:
            session.add(session_fact_tweet)
            session.commit()
            return session_fact_tweet

    def update_sentiment(self, tweet_id: str, sentiment: int):
        with self.session as session:
            for c in session.query(models.Fact_tweet).all():
                if c.tweet_id == tweet_id:
                    c.sentiment = sentiment
                    break
            session.commit()


class SubjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_subject(self, subject: str):
        with self.session as session:
            return session.query(models.Subject.name).filter(models.Subject.name == subject).first()

    def get_subject_id(self, subject: str):
        with self.session as session:
            return session.query(models.Subject.id).filter(models.Subject.name == subject).first()

    def get_subject_with_keyword(self, keyword: str):
        with self.session as session:
            return session.query(models.Subject.name).join(models.Keyword).filter(
                models.Subject.id == models.Keyword.subject_id,
                models.Keyword.name == keyword).all()

    def insert_subject(self, subject: str):
        with self.session as session:
            subject_id = str(abs(hash(subject)))
            session_subject = models.Subject(id=subject_id, name=subject)
            session.add(session_subject)
            session.commit()
            return session_subject


class KeywordRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_keyword_with_subject(self, subject: str):
        with self.session as session:
            return session.query(models.Keyword.name).join(models.Subject).filter(
                models.Subject.id == models.Keyword.subject_id,
                models.Subject.name == subject).all()

    def get_keyword_with_this_subject(self, keyword: str, subject: str):
        with self.session as session:
            return session.query(models.Keyword.name).join(models.Subject).filter(
                models.Keyword.name == keyword,
                models.Keyword.subject_id == models.Subject.id,
                models.Subject.name == subject
            ).first()

    def get_keyword(self, keyword: str):
        with self.session as session:
            return session.query(models.Keyword.name).filter(models.Keyword.name == keyword).first()

    def insert_keyword_with_this_subject(self, keyword: str, subject: str):
        with self.session as session:
            subject_id = session.query(models.Subject.id).filter(models.Subject.name == subject).first()
            keyword_id = str(abs(hash(keyword)))
            session_keyword = models.Keyword(id=keyword_id, subject_id=subject_id, name=keyword)
            session.add(session_keyword)
            session.commit()
            return session_keyword

    def update_positive_keyword(self, keyword: str, positive: int):
        with self.session as session:
            for c in session.query(models.Keyword).all():
                if c.name == keyword:
                    c.positive = positive
                    break
            session.commit()


class DateRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_date(self, date_id: str):
        with self.session as session:
            return session.query(models.Date).filter(models.Date.id == date_id).first()

    def insert_date(self, date_id, month, day, year, hour, minus, period, day_in_week):
        # id, month, day, year, hour, minus, period, day_in_week = date_values
        session_date = models.Date(id=date_id, month=month, day=day, year=year, hour=hour,
                                   minus=minus, period=period, day_in_week=day_in_week)
        with self.session as session:
            session.add(session_date)
            session.commit()
            return session_date
