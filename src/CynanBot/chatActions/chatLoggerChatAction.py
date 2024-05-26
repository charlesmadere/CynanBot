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
        if not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')

        self.__chatLogger: ChatLoggerInterface = chatLogger

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.isChatLoggingEnabled():
            return False

        msg = utils.cleanStr(message.getContent())

        self.__chatLogger.logMessage(
            msg = msg,
            twitchChannel = user.getHandle(),
            twitchChannelId = await message.getTwitchChannelId(),
            userId = message.getAuthorId(),
            userName = message.getAuthorName()
        )

        return True
