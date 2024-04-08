from abc import ABC, abstractmethod

from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userInterface import UserInterface


class AbsChatAction(ABC):

    @abstractmethod
    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        pass
