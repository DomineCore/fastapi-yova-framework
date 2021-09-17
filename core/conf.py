from sys import modules
from typing import Optional
from importlib import reload
class Config(object):
    
    @classmethod
    def set_config(cls, settings):
        configs = getattr(settings)
        for config in configs.items():
            setattr(cls, config[0], config[1])
