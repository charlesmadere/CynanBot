from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

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
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def websocketOutcomeColorToEventData(
        self,
        color: TwitchOutcomeColor
    ) -> Dict[str, int]:
        pass

    @abstractmethod
    async def websocketOutcomesToEventDataArray(
        self,
        outcomes: List[TwitchOutcome]
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def websocketSubscriptionTypeToString(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> str:
        pass
