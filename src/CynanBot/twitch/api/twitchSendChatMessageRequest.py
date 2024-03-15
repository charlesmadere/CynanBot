from typing import Any

import CynanBot.misc.utils as utils


class TwitchSendChatMessageRequest():

    def __init__(
        self,
        broadcasterId: str,
        message: str,
        replyParentMessageId: str | None,
        senderId: str,
    ):
        if not utils.isValidStr(broadcasterId):
            raise TypeError(f'broadcasterId argument is malformed: \"{broadcasterId}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif replyParentMessageId is not None and not isinstance(replyParentMessageId, str):
            raise TypeError(f'replyParentMessageId argument is malformed: \"{replyParentMessageId}\"')
        elif not utils.isValidStr(senderId):
            raise TypeError(f'senderId argument is malformed: \"{senderId}\"')

        self.__broadcasterId: str = broadcasterId
        self.__message: str = message
        self.__replyParentMessageId: str | None = replyParentMessageId
        self.__senderId: str = senderId

    def getBroadcasterId(self) -> str:
        return self.__broadcasterId

    def getMessage(self) -> str:
        return self.__message

    def getReplyParentMessageId(self) -> str | None:
        return self.__replyParentMessageId

    def getSenderId(self) -> str:
        return self.__senderId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'broadcasterId': self.__broadcasterId,
            'message': self.__message,
            'replyParentMessageId': self.__replyParentMessageId,
            'senderId': self.__senderId
        }
