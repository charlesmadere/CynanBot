import CynanBot.misc.utils as utils
from typing import Any


class TwitchChatDropReason():

    def __init__(
        self,
        code: str,
        message: str | None
    ):
        if not utils.isValidStr(code):
            raise TypeError(f'code argument is malformed: \"{code}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        self.__code: str = code
        self.__message: str | None = message

    def getCode(self) -> str:
        return self.__code

    def getMessage(self) -> str | None:
        return self.__message

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'code': self.__code,
            'message': self.__message
        }
