from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userInterface import UserInterface


class ChatLoggerChatAction(AbsChatAction):

    def __init__(
        self,
        chatLogger: ChatLoggerInterface
    ):
        assert isinstance(chatLogger, ChatLoggerInterface), f"malformed {chatLogger=}"

        self.__chatLogger: ChatLoggerInterface = chatLogger

    async def handleChat(
        self,
        mostRecentChat: Optional[MostRecentChat],
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.isChatLoggingEnabled():
            return False

        self.__chatLogger.logMessage(
            twitchChannel = user.getHandle(),
            userId = message.getAuthorId(),
            userName = message.getAuthorName(),
            msg = utils.cleanStr(message.getContent())
        )

        return True
