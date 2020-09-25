
from database.dml.database import Base


User = Base.classes.userr
'''
     Column      |          Type          | Collation | Nullable | Default 
-----------------+------------------------+-----------+----------+---------
 id              | character varying(19)  |           | not null | 
 name            | character varying(50)  |           | not null | 
 screen_name     | character varying(50)  |           |          | 
 description     | character varying(200) |           |          | 
 followers_count | integer                |           |          | 0
 friends_count   | integer                |           |          | 0
 status_count    | integer                |           |          | 0
 language        | character varying(10)  |           |          | 
 date_created_id | character varying(19)  |           |          | 
Indexes:
    "userr_pkey" PRIMARY KEY, btree (id)
    "userr_screen_name_key" UNIQUE CONSTRAINT, btree (screen_name)
Foreign-key constraints:
    "userr_date_created_id_fkey" 
        FOREIGN KEY (date_created_id) REFERENCES date(id)
Referenced by:
    TABLE "fact_tweet" CONSTRAINT "fact_tweet_user_id_fkey" 
        FOREIGN KEY (user_id) REFERENCES userr(id)

'''

Fact_tweet = Base.classes.fact_tweet
'''
     Column      |          Type          | Collation | Nullable | Default 
-----------------+------------------------+-----------+----------+---------
 tweet_id        | character varying(19)  |           | not null | 
 user_id         | character varying(19)  |           | not null | 
 subject_id      | character varying(19)  |           | not null | 
 date_created_id | character varying(19)  |           | not null | 
 text            | character varying(400) |           |          | 
 source          | character varying(15)  |           |          | 
 language        | character varying(5)   |           |          | 
 sentiment       | integer                |           |          | 0
Indexes:
    "fact_tweet_pkey" PRIMARY KEY, btree (tweet_id)
Foreign-key constraints:
    "fact_tweet_date_created_id_fkey" 
        FOREIGN KEY (date_created_id) REFERENCES date(id)
    "fact_tweet_subject_id_fkey" 
        FOREIGN KEY (subject_id) REFERENCES subject(id)
    "fact_tweet_user_id_fkey" 
        FOREIGN KEY (user_id) REFERENCES userr(id)
'''

Date = Base.classes.date
'''
   Column    |         Type          | Collation | Nullable | Default 
-------------+-----------------------+-----------+----------+---------
 id          | character varying(19) |           | not null | 
 month       | integer               |           | not null | 
 day         | integer               |           | not null | 
 year        | integer               |           | not null | 
 hour        | integer               |           | not null | 
 minus       | integer               |           | not null | 
 period      | integer               |           | not null | 
 day_in_week | character varying(10) |           | not null | 
Indexes:
    "date_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "fact_tweet" CONSTRAINT "fact_tweet_date_created_id_fkey" 
        FOREIGN KEY (date_created_id) REFERENCES date(id)
    TABLE "userr" CONSTRAINT "userr_date_created_id_fkey" 
        FOREIGN KEY (date_created_id) REFERENCES date(id)
'''

Keyword = Base.classes.keyword
'''
   Column   |         Type          | Collation | Nullable | Default 
------------+-----------------------+-----------+----------+---------
 id         | character varying(19) |           | not null | 
 subject_id | character varying(19) |           | not null | 
 name       | character varying(19) |           |          | 
 positive   | integer               |           |          | 0
Indexes:
    "keyword_pkey" PRIMARY KEY, btree (id, subject_id)
    "keyword_name_key" UNIQUE CONSTRAINT, btree (name)
Foreign-key constraints:
    "keyword_subject_id_fkey" 
        FOREIGN KEY (subject_id) REFERENCES subject(id)
'''

Subject = Base.classes.subject
'''
 Column |         Type          | Collation | Nullable | Default 
--------+-----------------------+-----------+----------+---------
 id     | character varying(19) |           | not null | 
 name   | character varying(19) |           |          | 
Indexes:
    "subject_pkey" PRIMARY KEY, btree (id)
    "subject_name_key" UNIQUE CONSTRAINT, btree (name)
Referenced by:
    TABLE "fact_tweet" CONSTRAINT "fact_tweet_subject_id_fkey" 
        FOREIGN KEY (subject_id) REFERENCES subject(id)
    TABLE "keyword" CONSTRAINT "keyword_subject_id_fkey" 
        FOREIGN KEY (subject_id) REFERENCES subject(id)
'''
