from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userInterface import UserInterface


class AbsChatAction(ABC):

    @abstractmethod
    async def handleChat(
        self,
        mostRecentChat: Optional[MostRecentChat],
        message: TwitchMessage,
        user: UserInterface
    ):
        pass
