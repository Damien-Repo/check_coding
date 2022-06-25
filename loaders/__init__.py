import os

from lib.utils import PluginManager
from .iloader import ILoader


class LoaderManager(PluginManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_plugins(ILoader, os.path.join('loaders', 'default'), 'loader_')
        self._load_plugins(ILoader, os.path.join(self.config.CUSTOM_ROOT_PATH, 'loaders'), 'loader_')

    def load_file(self, file_name):
        for _, cur_loader in self:
            cur_loader.parse(file_name)
