import os

from lib.utils import PluginManager, Singleton
from .default import DefaultConfig


class IConfigLoader:
    DUMP_MODE = 'str'

    @classmethod
    def check_type(cls, conf_file):
        if conf_file is None or conf_file == '':
            return True

    @classmethod
    def load_from_file(cls, conf_file):
        assert (cls.check_type(conf_file))
        return DefaultConfig

    @classmethod
    def dump(cls, conf):
        def _rec(data: dict, indent=0):
            out = f'{" " * indent}class {list(data.keys())[0]}:\n'
            for members in data.values():
                for k, v in members.items():
                    if isinstance(v, dict):
                        out += _rec({k: v}, indent + 1)
                    else:
                        out += f'{" " * indent} - {k} = {repr(v)}\n'
            return out
        return _rec(conf.dump_data())


class ConfigManager(PluginManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_plugins(IConfigLoader, os.path.join('lib', 'config'), 'config_loader_')

        self._loaded_conf = None

    def load_from_file(self, conf_file):
        self._loaded_conf = DefaultConfig
        for name, conf in self:
            if conf.check_type(conf_file):
                self._loaded_conf = conf.load_from_file(conf_file)
                break
        return self._loaded_conf

    def dump(self, mode=None):
        # Check None, False, and empty string
        if not mode:
            mode = IConfigLoader.DUMP_MODE

        if self._loaded_conf is not None:
            for name, conf_loader in self:
                if conf_loader.DUMP_MODE == mode:
                    f = getattr(conf_loader, f'dump', None)
                    if f is not None:
                        return f(self._loaded_conf)


class Config(metaclass=Singleton):

    def __init__(self, conf_file):
        self._manager = ConfigManager()
        self._conf = None
        self.load_from_file(conf_file)

    def __getattr__(self, item):
        return getattr(self._conf, item)

    def __str__(self):
        return self._manager.dump('str')

    def load_from_file(self, conf_file):
        self._conf = self._manager.load_from_file(conf_file)
        assert(self._conf is not None)

    def dump(self, mode='str'):
        return self._manager.dump(mode)


__all__ = ['Config', 'DefaultConfig']
