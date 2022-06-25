import os
import importlib


class Config:
    CUSTOM_ROOT_PATH = 'custom'

    class Loader:
        class Clang:
            LIB_PATH = None

    @staticmethod
    def _load_from_py(conf_file: str):
        conf_file = os.path.splitext(conf_file)[0]
        module_str = conf_file.replace(os.path.sep, '.')
        module = importlib.import_module(module_str)

        for name in dir(module):
            cls = getattr(module, name)
            if isinstance(cls, type) and issubclass(cls, Config) and cls != Config:
                return cls

    @staticmethod
    def load(conf_file: str):
        if conf_file is None or conf_file == '':
            return Config

        if conf_file.endswith('.py'):
            cls = Config._load_from_py(conf_file)

        return cls if cls is not None else Config
