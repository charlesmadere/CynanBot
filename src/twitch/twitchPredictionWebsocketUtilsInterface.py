from abc import ABC, abstractmethod
from typing import Any

from .api.twitchOutcome import TwitchOutcome
from .api.twitchOutcomeColor import TwitchOutcomeColor
from .api.websocket.twitchWebsocketEvent import TwitchWebsocketEvent
from .api.websocket.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType


class TwitchPredictionWebsocketUtilsInterface(ABC):

    @abstractmethod
    async def websocketEventToEventDataDictionary(
        self,
        event: TwitchWebsocketEvent,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> dict[str, Any] | None:
        pass

    @abstractmethod
    async def outcomeColorToEventData(
        self,
        color: TwitchOutcomeColor
    ) -> dict[str, int]:
        pass

    @abstractmethod
    async def outcomesToEventDataArray(
        self,
        outcomes: list[TwitchOutcome]
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def websocketSubscriptionTypeToString(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> str:
        pass
