from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class SessionModel(Base):
    __tablename__ = 'sessions'

    session_id = Column(Integer, primary_key=True, index=True)
    session_date = Column(Date)
    type_of_control = Column(String)
    teacher = Column(String, nullable=True)
    gruppa_id = Column(Integer, ForeignKey('gruppa.id_gruppa'))
    subject_id = Column(Integer, ForeignKey('subject.id_subject'))

    gruppa = relationship('Gruppa', back_populates="sessions")
    subject = relationship('Subject', back_populates="sessions")

class Gruppa(Base):
    __tablename__ = 'gruppa'

    id_gruppa = Column(Integer, primary_key=True, index=True)
    gruppa_code = Column(Integer)
    course = Column(Integer)
    faculty = Column(String)

    sessions = relationship('SessionModel', back_populates="gruppa")

class Subject(Base):
    __tablename__ = 'subject'

    id_subject = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    departament = Column(String, nullable=True)
    volume_of_hours = Column(Integer)

    sessions = relationship('SessionModel', back_populates="subject")