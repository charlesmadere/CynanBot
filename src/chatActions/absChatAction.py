from abc import ABC, abstractmethod

from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface


class AbsChatAction(ABC):

    @abstractmethod
    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface,
    ) -> bool:
        pass
