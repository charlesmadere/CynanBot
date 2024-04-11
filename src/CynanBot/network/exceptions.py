import CynanBot.misc.utils as utils


class GenericNetworkException(Exception):

    def __init__(self, message: str, statusCode: int | None = None):
        super().__init__(message)

        if statusCode is not None and not utils.isValidInt(statusCode):
            raise TypeError(f'statusCode argument is malformed: \"{statusCode}\"')

        self.__statusCode: int | None = statusCode

    def getStatusCode(self) -> int | None:
        return self.__statusCode


class NetworkResponseIsClosedException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
