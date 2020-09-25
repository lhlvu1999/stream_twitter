from streaming.apps import app, input_topic, analyze_topic
from streaming.processor import count_sports, clean_data_from_tweet


@app.agent(input_topic)
async def get_tweets(stream):
    # get all tweet in 10second to clean
    async for tweets in stream.take(100000, within=10):
        sports_in_period = clean_data_from_tweet(tweets)
        await analyze_topic.send(value=sports_in_period)


@app.agent(analyze_topic)
async def count_sports_post(sports_static):
    # create a list to store last 10 period time
    last_10_period_football = [0 for _ in range(10)]
    last_10_period_sports = [0 for _ in range(10)]
    async for event in sports_static:
        result = \
            count_sports(event, football=last_10_period_football, sports=last_10_period_sports)
        last_10_period_football, last_10_period_sports = result


if __name__ == '__main__':
    app.main()
