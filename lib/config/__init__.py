import os

from lib.utils import PluginManager, Singleton
from .default.default import DefaultConfig
from .loaders.config_loader_python import ConfigLoaderPython
from .iconfig import IConfigLoader


class ConfigManager(PluginManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_plugins(IConfigLoader, os.path.join('lib', 'config', 'loaders'), 'config_loader_')

        self._loaded_conf = None

    def load_from_file(self, conf_file):
        if conf_file is None:
            with open(os.path.join('lib', 'config', 'default', 'default.py'), 'r', encoding='utf-8') as f:
                self._loaded_conf = ConfigLoaderPython().load_from_file(f)
        else:
            for _, conf in self:
                if conf.check_type(conf_file):
                    self._loaded_conf = conf.load_from_file(conf_file)
                    break

        return self._loaded_conf

    def dump(self, mode=None):
        # Check None, False, and empty string
        if not mode:
            mode = IConfigLoader.DUMP_MODE

        if self._loaded_conf is not None:
            for _, conf_loader in self:
                if conf_loader.DUMP_MODE == mode:
                    f = getattr(conf_loader, 'dump', None)
                    if f is not None:
                        return f(self._loaded_conf)


class Config(metaclass=Singleton):

    def __init__(self, conf_file=None):
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

    def load_from_data(self, data: dict):
        assert(data is not None)
        self._conf.load_from_data(**data)

    def update_from_data(self, data: dict):
        assert(data is not None)
        self._conf.load_from_data(force=True, **data)

    def dump(self, mode='str'):
        return self._manager.dump(mode)


__all__ = ['Config', 'DefaultConfig']
