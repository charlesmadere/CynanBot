from abc import ABC, abstractmethod

from twitch.twitchConfigurationType import TwitchConfigurationType


class TwitchMessageable(ABC):

    @abstractmethod
    def getTwitchChannelName(self) -> str:
        pass

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    @abstractmethod
    async def send(self, message: str):
        pass
