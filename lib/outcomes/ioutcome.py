from lib.config import Config


class IOutcome:

    def __init__(self, config=Config):
        self.config = config

    def print(self, msg):
        pass

    def error(self, msg):
        pass

    def warning(self, msg):
        pass

    def info(self, msg):
        pass

    def debug(self, msg):
        pass

    def progress_start(self, title='', total_size=None, unit='', *args, **kwargs):
        pass

    def progress_set_name(self, name, *args, **kwargs):
        pass

    def progress_update(self, *args, **kwargs):
        pass

    def progress_stop(self, *args, **kwargs):
        pass

    def set_result(self, check_exception, *args, **kwargs):
        pass

    def get_outcome(self):
        pass
