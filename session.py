import psycopg2

db_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'anna2021',
    'host': '127.0.0.1',
    'port': 5432,
}


table_creation_query = """
CREATE TABLE IF NOT EXISTS session (
    session_id SERIAL PRIMARY KEY,
    session_date DATE,
    type_of_control VARCHAR(50) NOT NULL,
    teacher TEXT,
    gruppa_id INT REFERENCES gruppa(id_gruppa), 
    subject_id INT REFERENCES subject(id_subject) 
);
"""

try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    print("Соединение с базой данных установлено.")


    cursor.execute(table_creation_query)
    connection.commit()
    print("Таблица 'session' успешно создана.")

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    if 'connection' in locals() and connection:
        cursor.close()
        connection.close()
        print("Соединение с базой данных закрыто.")
