import uvicorn
import sys
import time
from fastapi import FastAPI, Request
from sqlmodel import SQLModel
import settings as conf

from routers import router

app = FastAPI()
app.include_router(router)

def make_models():
    SQLModel.metadata.create_all(conf.engine)


if __name__=='__main__':
    make_models()
    try:
        host = sys.argv[1]
        port = sys.argv[2]
        uvicorn.run(app, host=host, port=int(port))
    except:
        uvicorn.run(app, host="127.0.0.1", port=8080)
