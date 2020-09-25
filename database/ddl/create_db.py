from database.ddl.execute_postgres import Postgres


def create_db(db_name):
    db = Postgres()
    db.create_db(db_name)
    db.close()


def create_table(db_name):
    db = Postgres(db_name)
    db.create_table()
    db.close()


db = 'twitterdb'
create_db(db)
create_table(db)
