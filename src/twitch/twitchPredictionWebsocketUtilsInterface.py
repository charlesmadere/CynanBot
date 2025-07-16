from abc import ABC, abstractmethod
from typing import Any, Collection

from frozenlist import FrozenList

from .api.models.twitchOutcome import TwitchOutcome
from .api.models.twitchOutcomeColor import TwitchOutcomeColor
from .api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType


class TwitchPredictionWebsocketUtilsInterface(ABC):

    @abstractmethod
    async def websocketEventToEventDataDictionary(
        self,
        outcomes: FrozenList[TwitchOutcome],
        eventId: str,
        title: str,
        subscriptionType: TwitchWebsocketSubscriptionType,
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
        outcomes: Collection[TwitchOutcome]
    ) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def websocketSubscriptionTypeToString(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> str:
        pass
