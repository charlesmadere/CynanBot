from abc import ABC, abstractmethod

from ...api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ....misc.clearable import Clearable


class TwitchWebsocketSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getLoggingLevel(self) -> bool:
        pass

    @abstractmethod
    async def getSubscriptionTypes(self) -> frozenset[TwitchWebsocketSubscriptionType]:
        pass

    @abstractmethod
    async def isChatEventToCheerEventSubscriptionFallbackEnabled(self) -> bool:
        pass
