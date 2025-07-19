from abc import ABC, abstractmethod

from ....misc.clearable import Clearable


class TwitchWebsocketSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getLoggingLevel(self) -> bool:
        pass

    @abstractmethod
    async def isChatEventToCheerEventSubscriptionFallbackEnabled(self) -> bool:
        pass
