import os
import sys

from lib.utils import PluginManager
from lib.config import Config

from .ifiletype import IFileType, FileTypeUnknown


class FileTypesManager(PluginManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        extra = {
            'prefix': 'filetype_',
            'whitelist': Config().FileTypes.WHITELIST,
            'blacklist': Config().FileTypes.BLACKLIST,
        }
        self.load_plugins(IFileType, os.path.join('lib', 'filetypes'), **extra)
        self.load_plugins(IFileType, os.path.join(Config().CUSTOM_ROOT_PATH, 'filetypes'), **extra)

        cur_module = sys.modules['lib.filetypes']
        all_types = {ft.__class__.__name__: ft for _, ft in self}
        globals().update(all_types)
        cur_module.__all__ = list(all_types)

    def get_file_type(self, file_name):
        for _, ft in self:
            if ft.pattern(file_name):
                return ft
        return FileTypeUnknown
