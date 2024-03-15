from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchChatDropReason import TwitchChatDropReason


class TwitchSendChatMessageResponse():

    def __init__(
        self,
        isSent: bool,
        messageId: str,
        dropReason: TwitchChatDropReason | None
    ):
        if not utils.isValidBool(isSent):
            raise TypeError(f'isSent argument is malformed: \"{isSent}\"')
        elif not utils.isValidStr(messageId):
            raise TypeError(f'messageId argument is malformed: \"{messageId}\"')
        elif dropReason is not None and not isinstance(dropReason, TwitchChatDropReason):
            raise TypeError(f'dropReason argument is malformed: \"{dropReason}\"')

        self.__isSent: bool = isSent
        self.__messageId: str = messageId
        self.__dropReason: TwitchChatDropReason | None = dropReason

    def isSent(self) -> bool:
        return self.__isSent

    def getDropReason(self) -> TwitchChatDropReason | None:
        return self.__dropReason

    def getMessageId(self) -> str:
        return self.__messageId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'dropReason': self.__dropReason,
            'isSent': self.__isSent,
            'messageId': self.__messageId
        }
