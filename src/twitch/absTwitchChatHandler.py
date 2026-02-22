from abc import ABC, abstractmethod

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .localModels.twitchChatMessage import TwitchChatMessage
from ..users.userInterface import UserInterface


class AbsTwitchChatHandler(ABC):

    @abstractmethod
    async def onNewChat(self, chatMessage: TwitchChatMessage):
        pass

    @abstractmethod
    async def onNewChatDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
