class CommodoreSamExecutableIsMissingException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class CommodoreSamFailedToGenerateSpeechFileException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
