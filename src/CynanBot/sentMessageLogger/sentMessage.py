import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.sentMessageLogger.messageMethod import MessageMethod


class SentMessage():

    def __init__(
        self,
        successfullySent: bool,
        numberOfRetries: int,
        exceptions: list[Exception] | None,
        messageMethod: MessageMethod,
        msg: str,
        twitchChannel: str
    ):
        if not utils.isValidBool(successfullySent):
            raise TypeError(f'successfullySent argument is malformed: \"{successfullySent}\"')
        elif not utils.isValidInt(numberOfRetries):
            raise TypeError(f'numberOfRetries argument is malformed: \"{numberOfRetries}\"')
        elif numberOfRetries < 0 or numberOfRetries > utils.getIntMaxSafeSize():
            raise ValueError(f'numberOfRetries argument is out of bounds: {numberOfRetries}')
        elif exceptions is not None and not isinstance(exceptions, list):
            raise TypeError(f'exceptions argument is malformed: \"{exceptions}\"')
        elif not isinstance(messageMethod, MessageMethod):
            raise TypeError(f'messageMethod argument is malformed: \"{messageMethod}\"')
        elif not utils.isValidStr(msg):
            raise TypeError(f'msg argument is malformed: \"{msg}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__successfullySent: bool = successfullySent
        self.__numberOfRetries: int = numberOfRetries
        self.__exceptions: list[Exception] | None = exceptions
        self.__messageMethod: MessageMethod = messageMethod
        self.__msg: str = msg
        self.__twitchChannel: str = twitchChannel
        self.__sdt: SimpleDateTime = SimpleDateTime()

    def getExceptions(self) -> list[Exception] | None:
        return self.__exceptions

    def getMessageMethod(self) -> MessageMethod:
        return self.__messageMethod

    def getMsg(self) -> str:
        return self.__msg

    def getNumberOfRetries(self) -> int:
        return self.__numberOfRetries

    def getSimpleDateTime(self) -> SimpleDateTime:
        return self.__sdt

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def wasSuccessfullySent(self) -> bool:
        return self.__successfullySent
