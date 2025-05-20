from sqlalchemy import Column, String, Integer, Numeric
from .database import Base
from typing import Optional

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

# class Skills(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     category: str
#     name: str

# class Education(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
