from database.dml.database import SessionLocal
from database.dml import query
from nltk.tokenize import TweetTokenizer
from textblob import TextBlob


class Sentiment:

    def __init__(self):
        self.sentiment = []

    # simple analysis
    def analysis(self):
        tknzr = TweetTokenizer()
        db = SessionLocal()
        texts = query.get_text(db, 0, 1000)
        # print(texts)
        for i, text in texts:
            words = ' '.join(tknzr.tokenize(text))
            analysis = TextBlob(words)
            # print(words)
            if analysis.sentiment.polarity > 0:
                point = 1
            elif analysis.sentiment.polarity < 0:
                point = -1
            else:
                point = 0

            self.sentiment.append((i, point))
        db.close()

    def update(self):
        db = SessionLocal()
        for i, point in self.sentiment:
            query.update_sentiment(db, i, point)
        db.close()

    @staticmethod
    def get():
        db = SessionLocal()
        points = query.get_sentiment(db, 0, 1000)
        df_point = []
        for point in points:
            df_point.append([point[0]])
        db.close()
        return df_point
