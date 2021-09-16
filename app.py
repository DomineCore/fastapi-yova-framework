from sqlite3.dbapi2 import NotSupportedError
from functools import wraps
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
    def __init__(self, command):
        message = "Command: `{command}` is not exist!".format(command=command)
        super().__init__(message)


class ApplicationCommand(object):
    
    def start(self, *args, **kwargs):
        return self.wait_command()

    def wait_command(self):
        module, command, *args = sys.argv
        self.dispatch_command(command, args)

    def dispatch_command(self, command, args=None):
        if not hasattr(self, command):
            raise CommandError(command)
        return getattr(self, command)(args)
    
    def help(self, *args, **kwargs):
        print("\n".join([
            "\n",
            "=====================================================",
            "1. runserver: start the web server with uvicorn.",
            "2. mkdb: make database's tables with SQLModel engine.",
            "=====================================================",
            "If we have not the command what you need, you can create a issue for us, or you can create a pull request.",
            "\n"
        ]))

    def runserver(self, agvs, *args, **kwargs):
        try:
            host = agvs[0]
            port = int(agvs[1])
        except IndexError:
            host = "127.0.0.1"
            port = 8000
        uvicorn.run(app, host=host, port=port)

    def mkdb(self, *args, **kwargs):
        SQLModel.metadata.create_all(conf.engine)


if __name__=='__main__':
    app = ApplicationCommand()
    app.start()
