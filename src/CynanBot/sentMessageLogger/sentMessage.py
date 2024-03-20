import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


class SentMessage():

    def __init__(
        self,
        successfullySent: bool,
        usedTwitchApi: bool,
        numberOfRetries: int,
        exceptions: list[Exception] | None,
        msg: str,
        twitchChannel: str
    ):
        if not utils.isValidBool(successfullySent):
            raise TypeError(f'successfullySent argument is malformed: \"{successfullySent}\"')
        elif not utils.isValidBool(usedTwitchApi):
            raise TypeError(f'usedTwitchApi argument is malformed: \"{usedTwitchApi}\"')
        elif not utils.isValidInt(numberOfRetries):
            raise TypeError(f'numberOfRetries argument is malformed: \"{numberOfRetries}\"')
        elif not utils.isValidStr(msg):
            raise TypeError(f'msg argument is malformed: \"{msg}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__successfullySent: bool = successfullySent
        self.__usedTwitchApi: bool = usedTwitchApi
        self.__numberOfRetries: int = numberOfRetries
        self.__exceptions: list[Exception] | None = exceptions
        self.__msg: str = msg
        self.__twitchChannel: str = twitchChannel
        self.__sdt: SimpleDateTime = SimpleDateTime()

    def getExceptions(self) -> list[Exception] | None:
        return self.__exceptions

    def getMsg(self) -> str:
        return self.__msg

    def getNumberOfRetries(self) -> int:
        return self.__numberOfRetries

    def getSimpleDateTime(self) -> SimpleDateTime:
        return self.__sdt

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def usedTwitchApi(self) -> bool:
        return self.__usedTwitchApi

    def wasSuccessfullySent(self) -> bool:
        return self.__successfullySent
