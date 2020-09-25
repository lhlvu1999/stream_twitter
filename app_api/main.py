from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database.dml import query
from database.dml.database import SessionLocal

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/users/')
def read_users(skip: int = 0, limit: int = 5, db: Session = Depends(get_db)):
    execute = query.UserRepository(db)
    users = execute.get_users(skip, limit)
    return users


@app.get('/users/{user_id}')
def read_user(user_id: str, db: Session = Depends(get_db)):
    execute = query.UserRepository(db)
    db_user = execute.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404,  detail="User not found")
    return db_user


@app.get('/tweets/')
def read_tweets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    execute = query.TweetRepository(db)
    tweets = execute.get_tweets(skip, limit)
    return tweets


@app.get('/tweets/{tweet_id}')
def read_user_post_tweet(tweet_id: str, db: Session = Depends(get_db)):
    execute = query.UserRepository(db)
    db_tweet = execute.get_user_post_tweet(tweet_id)
    if db_tweet is None:
        raise HTTPException(status_code=404, detail="Tweet not found")
    return db_tweet


@app.get('/tweets/')
def read_tweets_with_subject(subject: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    execute = query.TweetRepository(db)
    tweets = execute.get_tweets_with_subject(subject, skip, limit)
    return tweets


@app.get('/read/subjects')
def read_subjects_with_keyword(keyword: str, db: Session = Depends(get_db)):
    execute = query.SubjectRepository(db)
    subjects = execute.get_subject_with_keyword(keyword)
    return subjects


@app.get('/read/keywords')
def read_keywords_with_subject(subject: str, db: Session = Depends(get_db)):
    execute = query.KeywordRepository(db)
    keywords = execute.get_keyword_with_subject(subject)
    return keywords


@app.put('/insert/subjects/')
def insert_new_subject(subject: str, db: Session = Depends(get_db)):
    execute = query.SubjectRepository(db)
    db_subject = execute.get_subject(subject)
    if db_subject:
        raise HTTPException(status_code=400, detail=f"{subject} already exists")
    return execute.insert_subject(subject)


@app.put('/insert/keywords/')
def insert_new_keyword(keyword: str, subject: str, db: Session = Depends(get_db)):
    execute = query.KeywordRepository(db)
    db_keyword = execute.get_keyword_with_this_subject(keyword, subject)
    if db_keyword:
        raise HTTPException(status_code=400, detail=f'{keyword} already in {subject}')
    return execute.insert_keyword_with_this_subject(keyword, subject)


@app.put('/update/keywords/positive')
def update_positive_keyword(keyword: str, positive: int, db: Session = Depends(get_db)):
    execute = query.KeywordRepository(db)
    db_keyword = execute.get_keyword(keyword)
    if not db_keyword:
        raise HTTPException(status_code=404, detail=f'{keyword} not found!')
    execute.update_positive_keyword(keyword, positive)
    return f'{keyword} has been update positive: {positive}'
