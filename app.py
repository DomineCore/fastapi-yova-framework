from sqlite3.dbapi2 import NotSupportedError
from functools import wraps
from sqlalchemy.sql.expression import except_all
import uvicorn
import sys
import types
import os
import time
from fastapi import FastAPI, Request, APIRouter
from typing import Optional
from importlib import import_module
from sqlmodel import SQLModel, create_engine

# from routers import router

class CommandError(Exception):
    def __init__(self, command):
        message = "Command: `{command}` is not exist!".format(command=command)
        super().__init__(message)

class AppNotExists(Exception):
    def __init__(self, app):
        message = "App: `{app}` is not exist!".format(app=app)
        super().__init__(message)

class AppIsNotDir(Exception):
    def __init__(self, app):
        message = "App: `{app}` is not a directory!".format(app=app)
        super().__init__(message)

class ApiMethodError(Exception):
    def __init__(self, method, path):
        message = "Method: `{method}` is not allowed in the `{path}`.".format(
            method=method,
            path=path
        )
        super().__init__(message)

class Application(object):
    def __init__(self, app=None):
        self.engine = create_engine("sqlite:///database.sqlite3")
        self.app = app
    
    def start(self, *args, **kwargs):
        return self.schedule_command()

    def schedule_command(self):
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
        uvicorn.run(self.app, host=host, port=port)

    def mkdb(self, *args, **kwargs):
        SQLModel.metadata.create_all(self.engine)

def add_api_router(
    app:Optional[FastAPI], 
    path:Optional[str], 
    methods:Optional[list], 
    view_func:Optional[types.FunctionType]
    ):
    for method in methods:
        if not hasattr(app, method):
            raise ApiMethodError
    app.router.add_api_route(path, view_func, methods=methods)

def init_config():
    from settings import Config
    # init_db
    DB_ENGINE_CONFIG = Config.DB_ENGINE_CONFIG
    engine = create_engine(url=DB_ENGINE_CONFIG["BACKEND"])
    setattr(Config, "db_engine", engine)
    return Config

def load_apps(configs):
    INSTALLED_APPS = configs.INSTALLED_APPS
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    # check app exists
    INSTALLED_APPS_PATH_LIST = []
    for APP in INSTALLED_APPS:
        APP_PATH = APP.replace('.','/')
        REAL_APP_PATH = os.path.join(PROJECT_ROOT, APP_PATH)
        if not os.path.exists(REAL_APP_PATH):
            raise AppNotExists(REAL_APP_PATH)
        if not os.path.isdir(REAL_APP_PATH):
            raise AppIsNotDir(REAL_APP_PATH)
        INSTALLED_APPS_PATH_LIST.append(REAL_APP_PATH)
    return INSTALLED_APPS_PATH_LIST, PROJECT_ROOT

def build_app(
    app_path_list:Optional[list],
    PROJECT_ROOT:Optional[str]
    ):
    fast_api_app = FastAPI()
    # build all app/urls.py
    urls_list = [
        import_module(
            os.path.join(app_path,'urls').lstrip(PROJECT_ROOT).replace('/','.').lstrip('.')
        )
        for app_path in app_path_list
        if os.path.exists(os.path.join(app_path, 'urls.py'))
    ]
    # build fastapi_routers
    for urls_module in urls_list:
        url_pattern = urls_module.url_pattern
        for url in url_pattern:
            path = url[0]
            view_func = url[1]
            methods = url[2]
            add_api_router(
                fast_api_app,
                path,
                methods,
                view_func
            )
    return fast_api_app

def WSB():
    # init settings config
    configs = init_config()
    # loading apps and inject configs to them
    apps,PROJECT_ROOT = load_apps(configs)
    # build fastapi app
    WSB_APP = build_app(apps,PROJECT_ROOT)
    # run the command_manager
    app_manager = Application(WSB_APP)
    app_manager.start()

if __name__=='__main__':
    """
    start the WSB_APP, wating for control.
    """
    WSB()

