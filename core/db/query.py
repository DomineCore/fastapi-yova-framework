from sqlmodel import Field, Session, SQLModel
from typing import Optional
from settings import Config

engine = Config.db_engine

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
    def delete(self, instance:Optional[SQLModel]):
        with Session(engine) as session:
            session.delete(instance)
            session.commit()
    
    @classmethod
    def update(self, pk:Optional[int], instance:Optional[SQLModel]):
        with Session(engine) as session:
            session.update(instance)
