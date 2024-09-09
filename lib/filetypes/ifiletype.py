

class IFileType:
    @staticmethod
    def pattern(file_name: str):
        raise NotImplementedError()


class FileTypeUnknown(IFileType):
    @staticmethod
    def pattern(_):
        return True
