from fastapi import APIRouter,Request
from home_application import models
from typing import Optional


router = APIRouter()

@router.post('/')
async def demo(person:Optional[models.Person],request:Request):
    person = dict(person)
    person = models.PersonSqlModel(**person)
    success = models.Cursor.create(person)
    return success