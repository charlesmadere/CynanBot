from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.simpleDateTime import SimpleDateTime


class SentMessage():

    def __init__(
        self,
        successfullySent: bool,
        numberOfRetries: int,
        exceptions: Optional[List[Exception]],
        msg: str,
        twitchChannel: str
    ):
        if not utils.isValidBool(successfullySent):
            raise ValueError(f'successfullySent argument is malformed: \"{successfullySent}\"')
        elif not utils.isValidInt(numberOfRetries):
            raise ValueError(f'numberOfRetries argument is malformed: \"{numberOfRetries}\"')
        elif not utils.isValidStr(msg):
            raise ValueError(f'msg argument is malformed: \"{msg}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__successfullySent: bool = successfullySent
        self.__numberOfRetries: int = numberOfRetries
        self.__exceptions: Optional[List[Exception]] = exceptions
        self.__msg: str = msg
        self.__twitchChannel: str = twitchChannel
        self.__sdt: SimpleDateTime = SimpleDateTime()

    def getExceptions(self) -> Optional[List[Exception]]:
        return self.__exceptions

    def getMsg(self) -> str:
        return self.__msg

    def getNumberOfRetries(self) -> int:
        return self.__numberOfRetries

    def getSimpleDateTime(self) -> SimpleDateTime:
        return self.__sdt

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def hasExceptions(self) -> bool:
        return utils.hasItems(self.__exceptions)

    def wasSuccessfullySent(self) -> bool:
        return self.__successfullySent
