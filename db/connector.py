import psycopg2
from config import config


def connect():
    connection = None
    try:
        params = config()
        print('Connecting to postgreSQL database . . .')
        connection = psycopg2.connect(**params)

        # create a cursor

        cursor = connection.cursor()
        print('PostgreSQL database version: ')
        cursor.execute("SELECT version()")
        db_version = cursor.fetchone()
        print(db_version)
        cursor.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("Database Connection Terminated")

connect()        