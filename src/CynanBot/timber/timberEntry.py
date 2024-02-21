from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


class TimberEntry():

    def __init__(
        self,
        tag: str,
        msg: str,
        exception: Optional[Exception] = None,
        traceback: Optional[str] = None
    ):
        if not utils.isValidStr(tag):
            raise ValueError(f'tag argument is malformed: \"{tag}\"')
        elif not utils.isValidStr(msg):
            raise ValueError(f'msg argument is malformed: \"{msg}\"')
        elif exception is not None and not isinstance(exception, Exception):
            raise ValueError(f'exception argument is malformed: \"{exception}\"')
        elif traceback is not None and not isinstance(traceback, str):
            raise ValueError(f'traceback argument is malformed: \"{traceback}\"')

        self.__tag: str = tag.strip()
        self.__msg: str = msg.strip()
        self.__exception: Optional[Exception] = exception
        self.__traceback: Optional[str] = traceback

        self.__sdt: SimpleDateTime = SimpleDateTime()

    def getException(self) -> Optional[Exception]:
        return self.__exception

    def getMsg(self) -> str:
        return self.__msg

    def getSimpleDateTime(self) -> SimpleDateTime:
        return self.__sdt

    def getTag(self) -> str:
        return self.__tag

    def getTraceback(self) -> Optional[str]:
        return self.__traceback

    def hasException(self) -> bool:
        return self.__exception is not None

    def hasTraceback(self) -> bool:
        return utils.isValidStr(self.__traceback)
