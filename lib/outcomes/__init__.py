import os

from lib.utils import PluginManager
from lib.config import Config
from .ioutcome import IOutcome


class OutcomeManager(PluginManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        extra = {
            'prefix': 'outcome_',
            'whitelist': Config().Outcome.WHITELIST,
            'blacklist': Config().Outcome.BLACKLIST,
        }

        self.load_plugins(IOutcome, os.path.join('lib', 'outcomes'), **extra)
        self.load_plugins(IOutcome, os.path.join(Config().CUSTOM_ROOT_PATH, 'outcomes'), **extra)
