from typing import Optional

import CynanBot.misc.utils as utils


class GenericNetworkException(Exception):

    def __init__(self, message: str, statusCode: Optional[int] = None):
        super().__init__(message)

        if statusCode is not None and not utils.isValidInt(statusCode):
            raise ValueError(f'statusCode argument is malformed: \"{statusCode}\"')

        self.__statusCode: Optional[int] = statusCode

    def getStatusCode(self) -> Optional[int]:
        return self.__statusCode

    def hasStatusCode(self) -> bool:
        return utils.isValidInt(self.__statusCode)


class NetworkResponseIsClosedException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
