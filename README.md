
# # # # Streaming Tweets Project # # # #

# # # # SCRIPT:

This project help us learn about a flow of data.
From a source (raw_data) through ETL process:
- Extract data using Tweet API
    - Transform data
    - Load data to:
        + Database
        + Kafka

In this project, we have 2 work:
- First:
    + Clean data from source and load to database (Postgres).
    + Create a function to sentiment analysis the packaged data (Tweet).
    + Create a API (fastAPI) to interact with database.
- Second:
    + Produce data from source to Kafka topic.
    + Modify data as what we need and send to a Faust topic.
    + Get data from faust topic to process real-time: visualize, analyze.

# # # # DESCRIPTION:

Firstly we must get data from source (Twitter) and cleaned before load.

To cleaned data, we must describe scenario and build database,
In database_packaged I have 2 folder:
   # ddl - Data Definition Language:
    execute_postgres.py:
    A class use psycopg2 library to make a database by execute query.
    My scenario has 5 table:
        .User_table (USERR):
            Store information about users: user_id, user_name, screen_user_name,
            created_date, language, description, followers_count, friends_count, status_count.
        .Fact_tweet_table (FACT_TWEET):
            Store information about tweets: tweet_id, user_id, text, language,
            created_date, source(device post tweet), sentiment_point.
        .Subject_table (SUBJECT):
            Store subjects that tweets talk about: subject_id, subject_name.
        .Keyword_table (KEYWORD):
            Store keywords relevant to subject: keyword_id, subject_id, keyword_name, positive_point.
        .Datetime_table (DATE):
            Store datetime: date_id, year, month, day, hour, minus, second, day_in_week.
    In this class, I have function:
        . __init__: Create a protocol connects to database.
        . create_db: Create a new database.
        . create_table: Create above scenario.
    create_db.py:
    Execute this file to createDB.
   # dml - Data Manipulation Language:
    I use sqlalchemy to help us interact db
    + database.py: we define the URL to connect db
    + models.py: we define variable map to table in db
    + query.py: I define function that support us to interact db


After build a database, we make a packaged to get tweets from twitter - stream_tweets_packaged:
   + twitter_credentials.py: In this file we save TOKEN and KEY to connect with twitter API
   + transports.py: We create a function stream() to process data, after that load clean_data to database and kafka.
       - insert_to_db: get specific attributes and insert to DB.
       - producer_kafka: get specific attributes and send to kafka topic.
   + catching_tweet.py: Use Tweepy library to get data from twitter API
       - class TwitterAuthenticator: return authentication after access TOKEN and KEY get from twitter_credentials.py.
       - TwitterStreamer: Streaming data.
       - TwitterListener: Listen data from twitter and transports.
   + stream_catching.py: We process this module with hash_tag_lists - subject of tweets that we want to get.

To help transform raw_data from twitter API, I create some class in helper folder
   + variable.py: I stored all list and dictionary variables
   + cleanData.py: A class to clean data:
       - class CleanData:
          * __init__: Transform raw_data to json type.
          * get_attribute: get specific attribute from data.
          * get_text: This text of tweet have many attributes, I want to get full of text, so I must check all of situation to get.
       - def convert_date:
            return a list [date_id, month, day, year, hour, minus, second, day_in_week]
                with date_id calculates from transforms date to second//10.
       - def filter_device:
            return a device that posted the tweet.
       - def clean_text:
            to make right form of text.
       - def convert_to_string:
            convert type of data to string type.
   + modify.py: create a class to modify data and ready to load to database and kafka.

While data is loading to database:
   - We create a analysis packaged to analyze data from DB:
        - sentimentAnalysis.py: A class to get sentiment from fact_tweet table and analyzed
            * simple_Analysis:
                + I use TweetTokenizer from nltk library to split text from tweet.
                + I use TextBlobs library to make a simple analysis Sentiment
            * update_Sentiment:
                + After analyzed, we update new sentiment point to database
            * get_Sentiment:
                + Get sentiment point of tweet from database
        - main.py: Execute analysis
   - We create a API (I using fastAPI) to interact our database - app_api packaged:
        - main.py: In this file, I define method of API to interact
        
While data is producing to kafka:
   - We use faust to consume stream from kafka topic
   - In streaming packaged:
        + kafka_streaming.py: Define a producer to produce data to kafka topic
        + class_stream.py: Define class use to get event and send event between topics
            * class Tweet: we define an event form kafka topic
            * class Sports: we define an event that we want to analyze
        + agent.py: Define agent use to listen topic and process stream
            * input_topic: We take all events from kafka topic each 10second to process
            * analyze_topic: We process event from an intermediaries topic
        + processor.py: Define process function
        + command.py: Define a consumer Faust to consume data from kafka topic

# # # # RUN:

To run project, we have follow in order of these commands:
# Before running project, we must have install environment:
    pip install -r requirement.txt
    
# 1. Running database

# 2. Create database, create table that we describe:
    python -m database.ddl.create_db

# 3. To run kafka, we have run zookeeper first, and then run kafka:
    $ tar -xzf kafka_2.13-2.6.0.tgz
    $ cd kafka_2.13-2.6.0
If not install kafka yet.
# Start the ZooKeeper service
    $ bin/zookeeper-server-start.sh config/zookeeper.properties
Open another terminal session and run:
# Start the Kafka broker service
    $ bin/kafka-server-start.sh config/server.properties
So before you can write your first events, you must create a topic.
# Open another terminal session and run:
    $ bin/kafka-topics.sh --create --topic topic_name --bootstrap-server localhost:9092

# 4. Run stream_tweets process to streaming data from twitter API:
    $ python -m stream_tweets.stream_catching

# 5. Open another terminal to process a faust streaming:
    $ python -m streaming.agent worker -l info

# 6. (Optional) To analysis sentiment from database:
    $ python -m analysis.main

# 7. To running fastAPI to interact with DB:
    $ uvicorn app_api.main:app --reload
# stream_twitter
