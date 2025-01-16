from abc import ABC, abstractmethod

from ..twitch.configuration.twitchContext import TwitchContext


class AbsChatCommand(ABC):

    @abstractmethod
    async def handleChatCommand(self, ctx: TwitchContext):
        pass
