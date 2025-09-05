from abc import ABC, abstractmethod

from ...twitch.configuration.twitchMessage import TwitchMessage


class ChatActionsManagerInterface(ABC):

    @abstractmethod
    async def handleMessage(self, message: TwitchMessage):
        pass
