from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Text, VARCHAR
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Gruppa(Base):
    __tablename__ = 'gruppa'

    id_gruppa = Column(Integer, primary_key=True, autoincrement=True)
    gruppa_code = Column(Integer)
    course = Column(Integer)
    faculty = Column(Text, nullable=False)

    sessions = relationship("Session", back_populates="gruppa")


class Subject(Base):
    __tablename__ = 'subject'

    id_subject = Column(Integer, primary_key=True, autoincrement=True)
    departament = Column(VARCHAR(70))
    name = Column(Text)
    volume_of_hours = Column(Integer)

    sessions = relationship("Session", back_populates="subject")


class Session(Base):
    __tablename__ = 'session'

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    session_date = Column(Date)
    type_of_control = Column(VARCHAR(50), nullable=False)
    teacher = Column(Text)
    gruppa_id = Column(Integer, ForeignKey('gruppa.id_gruppa'))
    subject_id = Column(Integer, ForeignKey('subject.id_subject'))

    gruppa = relationship("Gruppa", back_populates="sessions")
    subject = relationship("Subject", back_populates="sessions")

