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
from fastapi import HTTPException



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

#  CRUD
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

@app.get("/sessions_by_teacher/{teacher_name}")
def get_sessions_by_teacher_route(teacher_name: str, db: Session = Depends(get_db)):
    sessions_details = get_sessions_by_teacher(db, teacher_name)
    # print_table(sessions_details)  
    return sessions_details

#JOIN 
@app.get("/sessions_with_details/")
def get_sessions_with_details(db: Session = Depends(get_db)):
    results = (
        db.query(SessionModel, Gruppa, Subject)
        .join(Gruppa, SessionModel.gruppa_id == Gruppa.id_gruppa)
        .join(Subject, SessionModel.subject_id == Subject.id_subject)
        .all()
    )
    return [
        {
            "session_id": session.session_id,
            "session_date": session.session_date,
            "type_of_control": session.type_of_control,
            "teacher": session.teacher,
            "gruppa_code": gruppa.gruppa_code,
            "faculty": gruppa.faculty,
            "subject_name": subject.name,
        }
        for session, gruppa, subject in results
    ]

# UPDATE
@app.put("/sessions/update_teacher/")
def update_teacher(min_course: int, new_teacher: str, db: Session = Depends(get_db)):
    affected_rows = (
        db.query(SessionModel)
        .join(Gruppa, SessionModel.gruppa_id == Gruppa.id_gruppa)
        .filter(Gruppa.course >= min_course)
        .update({SessionModel.teacher: new_teacher}, synchronize_session=False)
    )
    db.commit()
    return {"updated_rows": affected_rows}

# GROUP BY
@app.get("/group_sessions_by_teacher/")
def group_sessions_by_teacher(db: Session = Depends(get_db)):
    results = (
        db.query(SessionModel.teacher, func.count(SessionModel.session_id).label("session_count"))
        .group_by(SessionModel.teacher)
        .all()
    )
    return [{"teacher": teacher, "session_count": count} for teacher, count in results]

# Сортировка результатов
@app.get("/sessions/sorted/")
def get_sorted_sessions(sort_by: str = "session_date", asc: bool = True, db: Session = Depends(get_db)):
    valid_columns = {
        "session_date": SessionModel.session_date,
        "teacher": SessionModel.teacher,
    }
    if sort_by not in valid_columns:
        raise HTTPException(status_code=400, detail=f"Invalid sort column: {sort_by}")
    query = db.query(SessionModel).order_by(
        valid_columns[sort_by].asc() if asc else valid_columns[sort_by].desc()
    )
    return query.all()



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
        with SessionLocal() as db_session:
            print("Начинается заполнение базы данных...")
            populate_data(db_session)  
            print("Заполнение завершено.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    connection = get_connection()
    populate_data(connection)


    # test_database() 
    # test_database_with_details()

if __name__ == "__main__":
     main() 









# тесты 

# #JOIN

# import requests
# import pandas as pd

# def test_database_with_details():
#     """
#     Тестирование эндпоинта /sessions_with_details/
#     """
#     url = "http://127.0.0.1:8000/sessions_with_details/"
#     try:
#         # Отправляем GET-запрос
#         response = requests.get(url)
        
#         # Проверяем успешность запроса
#         if response.status_code != 200:
#             print(f"Ошибка запроса: {response.status_code}, {response.text}")
#             return

#         # Преобразуем ответ в JSON
#         data = response.json()

#         # Создаем DataFrame для отображения
#         df = pd.DataFrame(data)
#         print(df)

#     except requests.exceptions.RequestException as e:
#         print(f"Ошибка при запросе к API: {e}")

# # SELECT
# def print_table(query_result):
#     data = []
#     for session in query_result:
#         data.append({
#             'Session ID': session.session_id,
#             'Session Date': session.session_date,
#             'Teacher': session.teacher,
#             'Gruppa ID': session.gruppa_id,
#             'Subject ID': session.subject_id,
#         })

#     df = pd.DataFrame(data)
    
#     print(df)

# def test_database():
#     db = SessionLocal() 
#     try:
#         sessions_details = get_sessions_by_teacher(db, "Dr. Brown")
#         print_table(sessions_details) 
#     finally:
#         db.close()  