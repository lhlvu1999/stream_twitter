import faust


class Tweet(faust.Record, serializer='json'):
    tweet_id: str
    text: str
    user_id: str
    source: str
    created_at: str
    lang: str


class Sports(faust.Record, serializer='json'):
    time: int
    football: int = 0
    all_sports: int = 0
