from lib.filetypes.ifiletype import IFileType


class FileTypeDotC(IFileType):
    @staticmethod
    def pattern(file_name: str):
        return file_name[-2:] == '.c'


class FileTypeDotH(IFileType):
    @staticmethod
    def pattern(file_name: str):
        return file_name[-2:] == '.h'
