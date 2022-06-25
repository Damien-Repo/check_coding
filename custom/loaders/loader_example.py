from loaders.iloader import ILoader
from lib.log import Log


class LoaderExample(ILoader):

    def _parse(self):
        Log().print(f"{self.__class__.__name__}: load '{self.file_name}'")
