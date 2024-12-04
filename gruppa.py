# -*- coding: utf-8 -*-
import psycopg2

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'anna2021',
    'host': '127.0.0.1',
    'port': 5432,
}

try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    print("Connected to the database.")

    table_creation_query = """
    CREATE TABLE IF NOT EXISTS gruppa (
        id_gruppa SERIAL PRIMARY KEY,
        gruppa_code INT,
        course INT,
        faculty TEXT NOT NULL
    );
    """
    cursor.execute(table_creation_query)
    connection.commit()
    print("Table 'gruppa' created successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()
        print("Database connection closed.")



