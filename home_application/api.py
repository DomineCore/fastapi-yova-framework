from typing import Optional
from home_application import models
from core.db.query import Cursor

async def save_person(person:Optional[models.Person]):
    try:
        Cursor.create(person)
    except Exception as e:
        return {
            "result":False,
            "code":"500",
            "message":"发生了一个小小的错误,不要慌,db模块加紧开发中"
        }
    return {
        "result":True,
        "code":"0",
        "data":person.name
    }

async def test_my_api(person:Optional[models.Person]):
    return {
        "result":True,
        "code":0,
        "data":{
            "name":person.name,
            "age":person.age
        }
    }
