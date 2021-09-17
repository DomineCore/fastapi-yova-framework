from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, select
from typing import Optional

"""
serializer-model
"""

class Person(BaseModel):
    name: str
    age: Optional[int] = 18


"""
db-model
"""

class PersonSqlModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None

