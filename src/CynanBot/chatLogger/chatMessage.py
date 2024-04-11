import CynanBot.misc.utils as utils
from CynanBot.chatLogger.absChatMessage import AbsChatMessage
from CynanBot.chatLogger.chatEventType import ChatEventType


class ChatMessage(AbsChatMessage):

    def __init__(
        self,
        msg: str,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        super().__init__(
            chatEventType = ChatEventType.MESSAGE,
            twitchChannel = twitchChannel
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

    def getMsg(self) -> str:
        return self.__msg

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
