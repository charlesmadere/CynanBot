from abc import ABC, abstractmethod
from typing import Any

from CynanBot.twitch.api.twitchOutcome import TwitchOutcome
from CynanBot.twitch.api.twitchOutcomeColor import TwitchOutcomeColor
from CynanBot.twitch.api.websocket.twitchWebsocketEvent import \
    TwitchWebsocketEvent
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType


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
