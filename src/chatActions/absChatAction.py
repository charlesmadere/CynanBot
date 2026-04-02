from abc import ABC, abstractmethod

from .chatActionResult import ChatActionResult
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class AbsChatAction(ABC):

    @property
    @abstractmethod
    def actionName(self) -> str:
        pass

    @abstractmethod
    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        pass
