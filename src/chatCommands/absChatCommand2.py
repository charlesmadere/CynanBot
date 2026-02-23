from abc import ABC, abstractmethod
from typing import Collection, Pattern

from .chatCommandResult import ChatCommandResult
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class AbsChatCommand2(ABC):

    @property
    @abstractmethod
    def commandPatterns(self) -> Collection[Pattern]:
        pass

    @abstractmethod
    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        pass
