import psycopg2
from .config import config


def connect():
    connection = None
    try:
        params = config()
        print('Connecting to PostgreSQL database . . .')
        connection = psycopg2.connect(**params)
        print("Connection successful.")
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        print("Database connection failed:", error)
        return None
