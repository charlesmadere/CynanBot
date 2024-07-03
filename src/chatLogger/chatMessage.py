from chatLogger.absChatMessage import AbsChatMessage
from chatLogger.chatEventType import ChatEventType
from misc.simpleDateTime import SimpleDateTime

from ..misc import utils as utils


class ChatMessage(AbsChatMessage):

    def __init__(
        self,
        dateTime: SimpleDateTime,
        msg: str,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str
    ):
        super().__init__(
            dateTime = dateTime,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidStr(msg):
            raise TypeError(f'msg argument is malformed: \"{msg}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__msg: str = msg
        self.__userId: str = userId
        self.__userName: str = userName

    @property
    def chatEventType(self) -> ChatEventType:
        return ChatEventType.MESSAGE

    @property
    def msg(self) -> str:
        return self.__msg

    @property
    def userId(self) -> str:
        return self.__userId

    @property
    def userName(self) -> str:
        return self.__userName
