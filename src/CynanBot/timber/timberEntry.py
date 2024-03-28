import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


class TimberEntry():

    def __init__(
        self,
        tag: str,
        msg: str,
        exception: Exception | None = None,
        traceback: str | None = None
    ):
        if not utils.isValidStr(tag):
            raise TypeError(f'tag argument is malformed: \"{tag}\"')
        elif not utils.isValidStr(msg):
            raise TypeError(f'msg argument is malformed: \"{msg}\"')
        elif exception is not None and not isinstance(exception, Exception):
            raise TypeError(f'exception argument is malformed: \"{exception}\"')
        elif traceback is not None and not isinstance(traceback, str):
            raise TypeError(f'traceback argument is malformed: \"{traceback}\"')

        self.__tag: str = tag.strip()
        self.__msg: str = msg.strip()
        self.__exception: Exception | None = exception
        self.__traceback: str | None = traceback

        self.__sdt: SimpleDateTime = SimpleDateTime()

    def getException(self) -> Exception | None:
        return self.__exception

    def getMsg(self) -> str:
        return self.__msg

    def getSimpleDateTime(self) -> SimpleDateTime:
        return self.__sdt

    def getTag(self) -> str:
        return self.__tag

    def getTraceback(self) -> str | None:
        return self.__traceback
