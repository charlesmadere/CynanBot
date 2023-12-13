from abc import ABC, abstractmethod

from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userInterface import UserInterface


class AbsChatAction(ABC):

    @abstractmethod
    async def handleChat(
        self,
        message: TwitchMessage,
        user: UserInterface
    ):
        pass
