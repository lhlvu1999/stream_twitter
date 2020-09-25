from helper.clean_data import CleanData


class Modify:

    def __init__(self, raw_data):
        data = CleanData(raw_data)
        self.dt = {
            'tweet_id': data.get_attribute(['id_str']),
            'user_id': data.get_attribute(['user', 'id_str']),
            'source': data.get_attribute(['source']),
            'text': data.get_text(),
            'name': data.get_attribute(['user', 'name']),
            'screen_name': data.get_attribute(['user', 'screen_name']),
            'followers_count': data.get_attribute(['user', 'followers_count']),
            'friends_count': data.get_attribute(['user', 'friends_count']),
            'description': data.get_attribute(['user', 'description']),
            'status_count': data.get_attribute(['user', 'statuses_count']),
            'date_user': data.get_attribute(['user', 'created_at']),
            'date_tweet': data.get_attribute(['created_at']),
            'lang_tweet': data.get_attribute(['lang']),
            'lang_user': data.get_attribute(['user', 'lang']),
            'subject': 'sports',
            'sentiment': 0,
        }

    def print_data(self):
        print(self.dt)

    def get_attribute(self, attribute):
        return self.dt[attribute]

    def get_subject(self):
        subject = self.dt['subject']
        return subject

    def get_user(self):
        data = self.dt
        user_id = data['user_id']
        name = data['name']
        screen_name = data['screen_name']
        description = data['description']
        followers_count = data['followers_count']
        friends_count = data['friends_count']
        status_count = data['status_count']
        lang_user = data['lang_user']
        date_user = data['date_user']
        return [user_id, name, screen_name, description, followers_count,
                friends_count, status_count, lang_user, date_user[0]]

    def get_tweet(self):
        data = self.dt
        tweet_id = data['tweet_id']
        user_id = data['user_id']
        subject_id = '0'
        date_tweet = data['date_tweet']
        text = data['text']
        source = data['source']
        lang_tweet = data['lang_tweet']
        return [tweet_id, user_id, subject_id, date_tweet[0],
                text, source, lang_tweet]

    def get_date_tweet(self):
        date = self.dt['date_tweet']
        return date

    def get_date_user(self):
        date = self.dt['date_user']
        return date

