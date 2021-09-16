from sqlite3.dbapi2 import NotSupportedError
from sqlalchemy.sql.expression import except_all
import uvicorn
import sys
import time
from fastapi import FastAPI, Request
from typing import Optional
from sqlmodel import SQLModel
import settings as conf

from routers import router

app = FastAPI()
app.include_router(router)

class CommandError(Exception):
    def __init__(self, message="Command is not exist!"):
        super().__init__(message)
        self.message = message


class ApplicationCommand(object):
    
    def start(self, *args, **kwargs):
        return self.wait_command()

    def wait_command(self):
        module, command, *args = sys.argv
        self.dispatch_command(command, args)

    def dispatch_command(self, command, args=None):
        if not hasattr(self, command):
            raise CommandError
        return getattr(self, command)(args)

    def runserver(self, args):
        try:
            host = args[0]
            port = int(args[1])
        except IndexError:
            host = "127.0.0.1"
            port = 8000
        uvicorn.run(app, host=host, port=port)

    def mkdb(self):
        SQLModel.metadata.create_all(conf.engine)


if __name__=='__main__':
    app = ApplicationCommand()
    app.start()
