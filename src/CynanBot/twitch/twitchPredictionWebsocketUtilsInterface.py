from abc import ABC, abstractmethod

from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType


class TwitchPredictionWebsocketUtilsInterface(ABC):

    @abstractmethod
    async def websocketSubscriptionTypeToString(
        self,
        subscriptionType: WebsocketSubscriptionType
    ) -> str:
        pass
