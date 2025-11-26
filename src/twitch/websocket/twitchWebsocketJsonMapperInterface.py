from abc import ABC, abstractmethod
from typing import Any

from .twitchWebsocketJsonLoggingLevel import TwitchWebsocketJsonLoggingLevel
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketEvent import TwitchWebsocketEvent
from ..api.models.twitchWebsocketSession import TwitchWebsocketSession
from ..api.models.twitchWebsocketSubscription import TwitchWebsocketSubscription


class TwitchWebsocketJsonMapperInterface(ABC):

    @abstractmethod
    async def parseLoggingLevel(
        self,
        loggingLevel: str | Any | None,
    ) -> TwitchWebsocketJsonLoggingLevel:
        pass

    @abstractmethod
    async def parseWebsocketDataBundle(
        self,
        dataBundleJson: dict[str, Any] | Any | None,
    ) -> TwitchWebsocketDataBundle | None:
        pass

    @abstractmethod
    async def parseWebsocketEvent(
        self,
        eventJson: dict[str, Any] | Any | None,
    ) -> TwitchWebsocketEvent | None:
        pass

    @abstractmethod
    async def parseWebsocketSession(
        self,
        sessionJson: dict[str, Any] | Any | None,
    ) -> TwitchWebsocketSession | None:
        pass

    @abstractmethod
    async def parseWebsocketSubscription(
        self,
        subscriptionJson: dict[str, Any] | Any | None,
    ) -> TwitchWebsocketSubscription | None:
        pass

    @abstractmethod
    async def serializeLoggingLevel(
        self,
        loggingLevel: TwitchWebsocketJsonLoggingLevel,
    ) -> str:
        pass
