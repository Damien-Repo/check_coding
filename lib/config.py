import os
import importlib

from lib.utils import Singleton


class DefaultConfig:
    CUSTOM_ROOT_PATH = 'custom'

    class Loader:
        class Clang:
            LIB_PATH = None

        class Raw:
            TAB_SIZE = None

    class Outcome:
        class Tqdm:
            class PrintColors:
                none = ''
                level = {
                    'ERRO': '',
                    'WARN': '',
                    'INFO': '',
                }
                src_file_name = ''
                line = ''
                checker_name = ''
                check_name = ''
                message = ''
                src_line = ''
                src_line_error = ''


class Config(metaclass=Singleton):

    def __init__(self, conf_file):
        #//TEMP gerer les differents loader de conf (PY, JSON, XML, etc.) comme les checkers, loaders, outcomes
        if conf_file is None or conf_file == '':
            self._conf = DefaultConfig
        elif conf_file.name.endswith('.py'):
            cls = self._load_from_py(conf_file.name)
            self._conf = cls if cls is not None else DefaultConfig

    def __getattr__(self, item):
        return getattr(self._conf, item)

    @staticmethod
    def _load_from_py(conf_file: str):
        conf_file = os.path.splitext(conf_file)[0]
        module_str = conf_file.replace(os.path.sep, '.')
        module = importlib.import_module(module_str)

        for name in dir(module):
            cls = getattr(module, name)
            if isinstance(cls, type) and issubclass(cls, Config) and cls != Config:
                return cls
