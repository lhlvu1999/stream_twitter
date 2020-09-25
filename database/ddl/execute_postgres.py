import psycopg2


class Postgres:

    def __init__(self):
        self.conn = psycopg2.connect(
            database='postgres', user='postgres',
            password='password', host='127.0.0.1', port='5432'
        )
        self.conn.autocommit = True
        # Creating a cursor object using the cursor() method
        self.cursor = self.conn.cursor()

    def create_db(self, db_name):
        # Preparing Query to create a database

        sql = 'CREATE database ' + db_name + ';'

        # Creating a database
        self.cursor.execute(sql)
        print("Database created successfully...")

    def create_table(self):
        # Dropping table if already exists.
        # Can not create 'user' table, so i used 'userr' instead
        self.cursor.execute("DROP TABLE IF EXISTS DATE, "
                            "USERR, SUBJECT, KEYWORD, FACT_TWEET;")

        # Creating table as per requirement
        sql = '''
        CREATE TABLE DATE(
            ID VARCHAR(19),
            MONTH INT NOT NULL,
            DAY INT NOT NULL,
            YEAR INT NOT NULL,
            HOUR INT NOT NULL,
            MINUS INT NOT NULL,
            PERIOD INT NOT NULL,
            DAY_IN_WEEK VARCHAR(10) NOT NULL,
            PRIMARY KEY (ID)
        );
        
        CREATE TABLE USERR(
            ID VARCHAR(19),
            NAME VARCHAR(50) NOT NULL,
            SCREEN_NAME VARCHAR(50) UNIQUE,
            DESCRIPTION VARCHAR(200),
            FOLLOWERS_COUNT INT DEFAULT 0,
            FRIENDS_COUNT INT DEFAULT 0,
            STATUS_COUNT INT DEFAULT 0,
            LANGUAGE VARCHAR(10),
            DATE_CREATED_ID VARCHAR(19),
            PRIMARY KEY (ID),
            FOREIGN KEY (DATE_CREATED_ID)
                REFERENCES DATE (ID)
        );
        
        CREATE TABLE SUBJECT(
            ID VARCHAR(19),
            NAME VARCHAR (19) UNIQUE,
            PRIMARY KEY (ID)
        );
        
        CREATE TABLE KEYWORD(
            ID VARCHAR(19),
            SUBJECT_ID VARCHAR(19),
            NAME VARCHAR (19) UNIQUE,
            POSITIVE INT DEFAULT 0,
            PRIMARY KEY (ID, SUBJECT_ID),
            FOREIGN KEY (SUBJECT_ID)
                REFERENCES SUBJECT (ID)
        );
        
        CREATE TABLE FACT_TWEET(
            TWEET_ID VARCHAR(19),
            USER_ID VARCHAR(19) NOT NULL,
            SUBJECT_ID VARCHAR(19) NOT NULL,
            DATE_CREATED_ID VARCHAR(19) NOT NULL,
            TEXT VARCHAR(400),
            SOURCE VARCHAR(15),
            LANGUAGE VARCHAR(5),
            SENTIMENT INT DEFAULT 0,
            PRIMARY KEY (TWEET_ID),
            FOREIGN KEY (USER_ID)
                REFERENCES USERR (ID),
            FOREIGN KEY (SUBJECT_ID)
                REFERENCES SUBJECT (ID),
            FOREIGN KEY (DATE_CREATED_ID)
                REFERENCES DATE (ID)
        )'''
        self.cursor.execute(sql)
        print("Table created successfully...")

    def close(self):
        self.conn.close()


'''
    def insert(self, table, insert_data):
        name_data = table_name[table]
        query = 'INSERT INTO ' + table + '('
        for i in range(len(name_data) - 1):
            # print(name_data[i], type(name_data[i]))
            query = query + name_data[i] + ','
        query = query + name_data[-1]+')'
        query = query + ' VALUES ('
        for i in range(len(insert_data) - 1):
            # print(type(insert_data[i]), insert_data[i])
            query = query + insert_data[i] + ','
        query = query + insert_data[-1] + ')'
        query = query + ' ON CONFLICT DO NOTHING;'
        # print(query)

        self.cursor.execute(query)

    def execute(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        # print(result)
        # self.conn.commit()
        return result

    def update(self, query):
        self.cursor.execute(query)
        self.conn.commit()
        return True

    def delete(self, query):
        pass
'''
