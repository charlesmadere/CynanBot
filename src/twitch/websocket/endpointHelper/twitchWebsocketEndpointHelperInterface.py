from abc import ABC, abstractmethod

from ..twitchWebsocketUser import TwitchWebsocketUser


class TwitchWebsocketEndpointHelperInterface(ABC):

    @abstractmethod
    def __getitem__(self, key: TwitchWebsocketUser) -> str:
        pass

    @abstractmethod
    def resetToDefault(self, key: TwitchWebsocketUser) -> str:
        pass

    @abstractmethod
    def __setitem__(self, key: TwitchWebsocketUser, value: str):
        pass
