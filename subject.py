import psycopg2

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'anna2021',
    'host': '127.0.0.1',
    'port': 5432,
}

table_creation_query = """
CREATE TABLE IF NOT EXISTS Subject (
    departament VARCHAR(70),
    id_subject SERIAL PRIMARY KEY,
    name TEXT,
    volume_of_hours INT
);
"""

try:

    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    print("Соединение с базой данных установлено.")

    
    cursor.execute(table_creation_query)
    connection.commit()
    print("Таблица 'Subject' успешно создана.")

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()
        print("Соединение с базой данных закрыто.")
