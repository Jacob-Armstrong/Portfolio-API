from sqlalchemy import Column, String, Integer, DateTime, func
from .database import Base

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    about = Column(String, nullable=False)
    favorite_color = Column(String, nullable=False)
    favorite_food = Column(String, nullable=False)

class Skills(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)

class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    school = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    major = Column(String, nullable=False)
    dates = Column(String, nullable=False)
    description = Column(String, nullable=False)

class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    dates = Column(String, nullable=False)
    description = Column(String, nullable=False)

class Visits(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    relation = Column(String, nullable=False)
    message = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.timezone('America/Los_Angeles', func.now()), nullable=False)