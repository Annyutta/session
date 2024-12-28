import psycopg2
from psycopg2 import sql

def get_connection():
    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='anna2021',
            host='127.0.0.1',
            port=5432,
        )
        return connection
    except psycopg2.Error as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None

