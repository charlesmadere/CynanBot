from abc import ABC, abstractmethod

from .twitchConfigurationType import TwitchConfigurationType


class TwitchMessageable(ABC):

    @abstractmethod
    async def getTwitchChannelId(self) -> str:
        pass

    @abstractmethod
    def getTwitchChannelName(self) -> str:
        pass

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    @abstractmethod
    async def send(self, message: str):
        pass
