import os

from lib.utils import PluginManager
from lib.config import Config
from .iloader import ILoader


class LoaderManager(PluginManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_plugins(ILoader, os.path.join('loaders', 'default'), 'loader_')
        self._load_plugins(ILoader, os.path.join(Config().CUSTOM_ROOT_PATH, 'loaders'), 'loader_')

    def load_file(self, file):
        for _, cur_loader in self:
            cur_loader.parse(file)

    def get_check_by(self):
        check_by = {}
        for _, cur_loader in self:
            check_by.update(cur_loader.CHECK_BY)
        return check_by
