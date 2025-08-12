from abc import ABC, abstractmethod

from ..twitchWebsocketUser import TwitchWebsocketUser


class TwitchWebsocketSubscriptionHelperInterface(ABC):

    @abstractmethod
    async def createEventSubSubscriptions(self, user: TwitchWebsocketUser):
        pass
