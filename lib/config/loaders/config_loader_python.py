import os
import importlib
import inspect

from ..iconfig import IConfig, IConfigLoader


class ConfigLoaderPython(IConfigLoader):
    DUMP_MODE = 'python'

    @classmethod
    def check_type(cls, conf_file):
        return getattr(conf_file, 'name', False) and conf_file.name.endswith('.py')

    @classmethod
    def load_from_file(cls, conf_file):
        assert(cls.check_type(conf_file))

        module_str = os.path.splitext(conf_file.name.replace(os.path.sep, '.'))[0]
        module = importlib.import_module(module_str)

        for name in [n for n, m in inspect.getmembers(module, inspect.isclass) if m.__module__ == module_str]:
            conf = getattr(module, name)
            if isinstance(conf, type) and issubclass(conf, IConfig) and conf != IConfig:
                return conf

    @classmethod
    def dump(cls, conf):
        def _rec(data: dict, indent=0):
            out = f'{"  " * indent}class {list(data.keys())[0]}():\n'
            for members in data.values():
                for k, v in members.items():
                    if isinstance(v, dict):
                        out += _rec({k: v}, indent + 1)
                    else:
                        out += f'{"  " * (indent + 1)}{k} = {repr(v)}\n'
            return out
        return _rec(conf.dump_data())[:-1]  # [:-1] to remove useless last '\n'
