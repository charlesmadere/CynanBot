from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from CynanBot.twitch.websocket.twitchWebsocketChannelPointsVoting import \
    TwitchWebsocketChannelPointsVoting
from CynanBot.twitch.websocket.websocketCommunitySubGift import \
    WebsocketCommunitySubGift
from CynanBot.twitch.websocket.websocketCondition import WebsocketCondition
from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.twitch.websocket.websocketEvent import WebsocketEvent
from CynanBot.twitch.websocket.websocketOutcome import WebsocketOutcome
from CynanBot.twitch.websocket.websocketOutcomePredictor import \
    WebsocketOutcomePredictor
from CynanBot.twitch.websocket.websocketReward import WebsocketReward
from CynanBot.twitch.websocket.websocketSession import WebsocketSession
from CynanBot.twitch.websocket.websocketSubGift import WebsocketSubGift
from CynanBot.twitch.websocket.websocketSubscription import \
    WebsocketSubscription


class TwitchWebsocketJsonMapperInterface(ABC):

    @abstractmethod
    async def parseWebsocketChannelPointsVoting(self, channelPointsVotingJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketChannelPointsVoting]:
        pass

    @abstractmethod
    async def parseWebsocketCommunitySubGift(self, giftJson: Optional[Dict[str, Any]]) -> Optional[WebsocketCommunitySubGift]:
        pass

    @abstractmethod
    async def parseWebsocketCondition(self, conditionJson: Optional[Dict[str, Any]]) -> Optional[WebsocketCondition]:
        pass

    @abstractmethod
    async def parseWebsocketDataBundle(self, dataBundleJson: Optional[Dict[str, Any]]) -> Optional[WebsocketDataBundle]:
        pass

    @abstractmethod
    async def parseWebsocketEvent(self, eventJson: Optional[Dict[str, Any]]) -> Optional[WebsocketEvent]:
        pass

    @abstractmethod
    async def parseWebsocketOutcome(self, outcomeJson: Optional[Dict[str, Any]]) -> Optional[WebsocketOutcome]:
        pass

    @abstractmethod
    async def parseWebsocketOutcomePredictor(self, predictorJson: Optional[Dict[str, Any]]) -> Optional[WebsocketOutcomePredictor]:
        pass

    @abstractmethod
    async def parseWebsocketReward(self, rewardJson: Optional[Dict[str, Any]]) -> Optional[WebsocketReward]:
        pass

    @abstractmethod
    async def parseWebsocketSession(self, sessionJson: Optional[Dict[str, Any]]) -> Optional[WebsocketSession]:
        pass

    @abstractmethod
    async def parseWebsocketSubGift(self, giftJson: Optional[Dict[str, Any]]) -> Optional[WebsocketSubGift]:
        pass

    @abstractmethod
    async def parseWebsocketSubscription(self, subscriptionJson: Optional[Dict[str, Any]]) -> Optional[WebsocketSubscription]:
        pass
