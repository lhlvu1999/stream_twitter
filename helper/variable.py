# # # # TABLE NAME # # # #
tweet_name = ['TWEET_ID', 'USER_ID', 'SUBJECT_ID',
              'DATE_CREATED_ID', 'TEXT', 'SOURCE', 'LANGUAGE']

user_name = ['ID', 'NAME', 'SCREEN_NAME', 'DESCRIPTION', 'FOLLOWERS_COUNT',
             'FRIENDS_COUNT', 'STATUS_COUNT', 'LANGUAGE', 'DATE_CREATED_ID']

subject_name = ['ID', 'NAME']

keyword_name = ['ID', 'SUBJECT_ID', 'POSITIVE']

date_name = ['ID', 'MONTH', 'DAY', 'YEAR', 'HOUR', 'MINUS', 'PERIOD', 'DAY_IN_WEEK']

table_name = {'FACT_TWEET': tweet_name, 'USERR': user_name,
              'SUBJECT': subject_name, 'KEYWORD': keyword_name, 'DATE': date_name}

# # # # DATE # # # #
month_trans = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
               'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
               'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

day_in_week_trans = {'Mon': 'Monday', 'Tue': 'Tuesday',
                     'Wed': 'Wednesday', 'Thu': 'Thursday',
                     'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}

# # # # DEVICE # # # #
devices = ['iPhone', 'Android', 'iPad', 'Web App', 'Mobile Web']

# # # # SUBJECT # # # #
sports = ['football', 'volleyball', 'basketball', 'golf', 'swim',
          'badminton', 'tennis', 'baseball', 'marathon', 'soccer']

second_to_period = 10
minus_to_period = 60 // second_to_period
hour_to_period = minus_to_period * 60
day_to_period = hour_to_period * 24
month_to_period = day_to_period * 31
year_to_period = month_to_period * 12
