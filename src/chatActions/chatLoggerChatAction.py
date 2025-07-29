from typing import Final

from .absChatAction import AbsChatAction
from ..chatLogger.chatLoggerInterface import ChatLoggerInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface


class ChatLoggerChatAction(AbsChatAction):

    def __init__(
        self,
        chatLogger: ChatLoggerInterface,
    ):
        if not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')

        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface,
    ) -> bool:
        if not user.isChatLoggingEnabled:
            return False

        cleanedMessage = utils.cleanStr(message.getContent())

        self.__chatLogger.logMessage(
            bits = None,
            chatterUserId = message.getAuthorId(),
            chatterUserLogin = message.getAuthorName(),
            message = cleanedMessage,
            twitchChannel = user.handle,
            twitchChannelId = await message.getTwitchChannelId(),
        )

        return True
