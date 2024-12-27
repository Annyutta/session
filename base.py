from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

def setup_database(connection_string):
    """Создаёт все таблицы в базе данных."""
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    print("Таблицы успешно созданы.")

if __name__ == "__main__":
    # Используем ваши данные для подключения
    connection_string = "postgresql+psycopg2://postgres:anna2021@127.0.0.1:5432/postgres"
    setup_database(connection_string)
