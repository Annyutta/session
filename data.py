from sqlalchemy.orm import Session
from models import Gruppa, Subject, SessionModel
import random
from datetime import datetime, timedelta

def generate_random_date(start_date: str, end_date: str) -> str:
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")

def create_random_groups(sessions: Session, n=5):
    for _ in range(n):
        group = Gruppa(
            gruppa_code=random.randint(1000, 9999),
            course=random.randint(1, 5),
            faculty=random.choice(["Science", "Arts", "Engineering"])
        )
        sessions.add(group)
    sessions.commit()

def create_random_subjects(sessions: Session, n=5):
    for _ in range(n):
        subject = Subject(
            name=random.choice(["Math", "Physics", "Chemistry", "History", "Biology"]),
            volume_of_hours=random.randint(30, 120)
        )
        sessions.add(subject)
    sessions.commit()

def create_random_sessions(sessions: Session, n=10):
    groups = sessions.query(Gruppa).all()
    subjects = sessions.query(Subject).all()

    for _ in range(n):
        new_session = SessionModel(
            session_date=generate_random_date("2023-01-01", "2023-12-31"),
            type_of_control=random.choice(["Exam", "Test", "Lab"]),
            teacher=random.choice(["Dr. Brown", "Prof. Smith", "Dr. Taylor"]),
            gruppa_id=random.choice(groups).id_gruppa,
            subject_id=random.choice(subjects).id_subject,
        )
        sessions.add(new_session)
    sessions.commit()

def populate_data(sessions: Session):
    try:
        create_random_groups(sessions)
        create_random_subjects(sessions)
        create_random_sessions(sessions)
    except Exception as e:
        print(f"Ошибка при добавлении данных: {e}")
        sessions.rollback()  
    finally:
        sessions.close()
