import subprocess
import pandas as pd
from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.orm import declarative_base
from data import populate_data
from server import get_connection
from models import Subject, SessionModel, Gruppa
from typing import List

DATABASE_URL = "postgresql+psycopg2://postgres:anna2021@127.0.0.1:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class SessionOut(BaseModel):
    session_id: int
    session_date: date
    type_of_control: str
    teacher: Optional[str]
    gruppa_id: int
    subject_id: int

    class Config:
        orm_mode = True

class GruppaOut(BaseModel):
    gruppa_code: int
    course: int
    faculty: str

    class Config:
        orm_mode = True

class SubjectOut(BaseModel):
    name: str
    volume_of_hours: int

    class Config:
        orm_mode = True


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sessions/", response_model=List[SessionOut])
def get_sessions(db: Session = Depends(get_db)):
    return db.query(SessionModel).all()

@app.post("/sessions/", response_model=SessionOut)
def create_session(session: SessionOut, db: Session = Depends(get_db)):
    new_session = SessionModel(**session.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@app.put("/sessions/{session_id}", response_model=SessionOut)
def update_session(session_id: int, session_data: SessionOut, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    for key, value in session_data.dict().items():
        setattr(session, key, value)
    db.commit()
    return session

@app.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(session)
    db.commit()
    return {"detail": "Session deleted successfully"}


# SELECT
def get_sessions_by_teacher(db: Session, teacher_name: str):
    return db.query(SessionModel).filter(SessionModel.teacher == teacher_name).all()
# # Function to print the table from the query result
def print_table(query_result):
    # Create a list of dictionaries from query result
    data = []
    for session in query_result:
        data.append({
            'Session ID': session.session_id,
            'Session Date': session.session_date,
            'Teacher': session.teacher,
            'Gruppa ID': session.gruppa_id,
            'Subject ID': session.subject_id,
        })

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(data)
    
    # Print the DataFrame as a table
    print(df)


@app.get("/sessions_by_teacher/{teacher_name}")
def get_sessions_by_teacher_route(teacher_name: str, db: Session = Depends(get_db)):
    sessions_details = get_sessions_by_teacher(db, teacher_name)
    # print_table(sessions_details)  # Печать таблицы
    return sessions_details

# This function is for testing the database select outside FastAPI
def test_database():
    db = SessionLocal()  # Manually create a session for testing outside FastAPI
    try:
        sessions_details = get_sessions_by_teacher(db, "Dr. Brown")
        print_table(sessions_details)  # Print the table
    finally:
        db.close()  # Ensure that the session is closed

def main():
    files_to_run = [ 
        "server.py",  
        "table.py",
        "models.py",
        "data.py"   
    ]

    for file in files_to_run:
        print(f"Запуск {file}...")
        result = subprocess.run(["python", file])
        
        if result.returncode != 0:
            print(f"Ошибка при выполнении {file}. Прервано.")
            break
        else:
            print(f"{file} успешно выполнен.")
    try:
        # Создаём сессию SQLAlchemy
        with SessionLocal() as db_session:
            print("Начинается заполнение базы данных...")
            populate_data(db_session)  # Передаём сессию SQLAlchemy
            print("Заполнение завершено.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    #     connection = get_connection()
    # populate_data(connection)


    test_database()  

if __name__ == "__main__":
     main() 
