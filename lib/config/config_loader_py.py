import os
import importlib

from . import IConfigLoader
from .default import DefaultConfig


class ConfigLoaderPy(IConfigLoader):
    @classmethod
    def check_type(cls, conf_file):
        return getattr(conf_file, 'name', False) and conf_file.name.endswith('.py')

    @classmethod
    def load_from_file(cls, conf_file):
        conf_file = os.path.splitext(conf_file.name)[0]
        module_str = conf_file.replace(os.path.sep, '.')
        module = importlib.import_module(module_str)

        for name in dir(module):
            cls = getattr(module, name)
            if isinstance(cls, type) and issubclass(cls, DefaultConfig) and cls != DefaultConfig:
                return cls
