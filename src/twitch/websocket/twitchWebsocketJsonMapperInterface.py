from abc import ABC, abstractmethod
from typing import Any

from .twitchWebsocketJsonLoggingLevel import TwitchWebsocketJsonLoggingLevel
from ..api.models.twitchOutcome import TwitchOutcome
from ..api.models.twitchSubGift import TwitchSubGift
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketEvent import TwitchWebsocketEvent
from ..api.models.twitchWebsocketSession import TwitchWebsocketSession
from ..api.models.twitchWebsocketSubscription import TwitchWebsocketSubscription


class TwitchWebsocketJsonMapperInterface(ABC):

    @abstractmethod
    async def parseLoggingLevel(
        self,
        loggingLevel: str | Any | None
    ) -> TwitchWebsocketJsonLoggingLevel:
        pass

    @abstractmethod
    async def parseWebsocketDataBundle(
        self,
        dataBundleJson: dict[str, Any] | None
    ) -> TwitchWebsocketDataBundle | None:
        pass

    @abstractmethod
    async def parseWebsocketEvent(
        self,
        eventJson: dict[str, Any] | None
    ) -> TwitchWebsocketEvent | None:
        pass

    @abstractmethod
    async def parseTwitchOutcome(
        self,
        outcomeJson: dict[str, Any] | None
    ) -> TwitchOutcome | None:
        pass

    @abstractmethod
    async def parseTwitchWebsocketSession(
        self,
        sessionJson: dict[str, Any] | None
    ) -> TwitchWebsocketSession | None:
        pass

    @abstractmethod
    async def parseWebsocketSubGift(
        self,
        giftJson: dict[str, Any] | None
    ) -> TwitchSubGift | None:
        pass

    @abstractmethod
    async def parseWebsocketSubscription(
        self,
        subscriptionJson: dict[str, Any] | None
    ) -> TwitchWebsocketSubscription | None:
        pass

    @abstractmethod
    async def serializeLoggingLevel(
        self,
        loggingLevel: TwitchWebsocketJsonLoggingLevel
    ) -> str:
        pass
