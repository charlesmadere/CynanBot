class FailedToChooseRandomTtsException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class NoEnabledTtsProvidersException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TtsProviderIsNotEnabledException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnableToParseUserMessageIntoTtsException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
