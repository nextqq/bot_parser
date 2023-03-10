from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class Task(BaseModel):
    __tablename__ = 'task'

    id = Column(String, primary_key=True)
    name = Column(String)
    difficulty = Column(Integer, default=0)
    answer_count = Column(Integer, default=0)


class TaskTypes(BaseModel):
    __tablename__ = 'task_type'

    id = Column(Integer, primary_key=True)
    task_id = Column(String, ForeignKey('task.id'), nullable=True)
    name = Column(String)
