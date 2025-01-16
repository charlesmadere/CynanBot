from abc import ABC, abstractmethod

from ..twitchWebsocketUser import TwitchWebsocketUser


class TwitchWebsocketInstabilityHelperInterface(ABC):

    @abstractmethod
    def __getitem__(self, key: TwitchWebsocketUser) -> int:
        pass

    @abstractmethod
    def incrementErrorCount(self, key: TwitchWebsocketUser) -> int:
        pass

    @abstractmethod
    def resetToDefault(self, key: TwitchWebsocketUser):
        pass
