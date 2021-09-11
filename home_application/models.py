from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel
from settings import engine
from typing import Optional

class Person(BaseModel):
    name: str
    age: Optional[int] = 18


class Cursor():

    @classmethod
    def create(self, instance:Optional[SQLModel]):
        with Session(engine) as session:
            session.add(instance)
            session.commit()

    @classmethod
    def bulk_create(self,instances:Optional[set]):
        with Session(engine) as session:
            for instance in instances:
                session.add(instance)
            session.commit()
    
    @classmethod
    def delete(self):
        pass

class PersonSqlModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str 
    age: Optional[int] = None

