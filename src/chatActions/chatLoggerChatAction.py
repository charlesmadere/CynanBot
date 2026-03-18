from typing import Final

from .absChatAction2 import AbsChatAction2
from .chatActionResult import ChatActionResult
from ..chatLogger.chatLoggerInterface import ChatLoggerInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class ChatLoggerChatAction(AbsChatAction2):

    def __init__(
        self,
        chatLogger: ChatLoggerInterface,
    ):
        if not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')

        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger

    @property
    def actionName(self) -> str:
        return 'ChatLoggerChatAction'

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        if not chatMessage.twitchUser.isChatLoggingEnabled:
            return ChatActionResult.IGNORED

        cleanedMessage = utils.cleanStr(chatMessage.text)

        self.__chatLogger.logMessage(
            bits = None,
            chatterUserId = chatMessage.chatterUserId,
            chatterUserLogin = chatMessage.chatterUserLogin,
            message = cleanedMessage,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        return ChatActionResult.HANDLED
