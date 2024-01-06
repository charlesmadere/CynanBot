from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from CynanBot.twitch.websocket.websocketEvent import WebsocketEvent
from CynanBot.twitch.websocket.websocketOutcome import WebsocketOutcome
from CynanBot.twitch.websocket.websocketOutcomeColor import \
    WebsocketOutcomeColor
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType


class TwitchPredictionWebsocketUtilsInterface(ABC):

    @abstractmethod
    async def websocketEventToEventDataDictionary(
        self,
        event: WebsocketEvent,
        subscriptionType: WebsocketSubscriptionType
    ) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def websocketOutcomeColorToString(
        self,
        color: WebsocketOutcomeColor
    ) -> str:
        pass

    @abstractmethod
    async def websocketOutcomesToEventDataArray(
        self,
        outcomes: List[WebsocketOutcome]
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def websocketSubscriptionTypeToString(
        self,
        subscriptionType: WebsocketSubscriptionType
    ) -> str:
        pass
