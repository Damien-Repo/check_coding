import os

from lib.utils import PluginManager
from lib.config import Config
from .iloader import ILoader


class LoaderManager(PluginManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        extra = {
            'prefix': 'loader_',
            'whitelist': Config().Loader.WHITELIST + ['default.LoaderRaw'],  # Enforce LoaderRaw (needed by core engine)
            'blacklist': Config().Loader.BLACKLIST,
        }
        self.load_plugins(ILoader, os.path.join('lib', 'loaders'), **extra)
        self.load_plugins(ILoader, os.path.join(Config().CUSTOM_ROOT_PATH, 'loaders'), **extra)

    def load_file(self, file, target):
        for _, cur_loader in self:
            cur_loader.parse(file, target)

    def get_check_by(self):
        check_by = {}
        for _, cur_loader in self:
            check_by.update(cur_loader.CHECK_BY)
        return check_by
