import os

from lib.utils import PluginManager
from lib.config import Config
from .ioutcome import IOutcome


class OutcomeManager(PluginManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_plugins(IOutcome, os.path.join('outcomes', 'default'), 'outcome_')
        self._load_plugins(IOutcome, os.path.join(Config().CUSTOM_ROOT_PATH, 'outcomes'), 'outcome_')

    def load_file(self, file_name):
        for _, cur_loader in self:
            cur_loader.parse(file_name)

    def get_check_by(self):
        check_by = {}
        for _, cur_loader in self:
            check_by.update(cur_loader.CHECK_BY)
        return check_by
