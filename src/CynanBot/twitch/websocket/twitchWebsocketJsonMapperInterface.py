from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from CynanBot.twitch.api.twitchCommunitySubGift import TwitchCommunitySubGift
from CynanBot.twitch.api.twitchOutcome import TwitchOutcome
from CynanBot.twitch.api.twitchOutcomePredictor import TwitchOutcomePredictor
from CynanBot.twitch.api.twitchPollChoice import TwitchPollChoice
from CynanBot.twitch.api.twitchReward import TwitchReward
from CynanBot.twitch.api.twitchSubGift import TwitchSubGift
from CynanBot.twitch.api.twitchWebsocketChannelPointsVoting import \
    TwitchChannelPointsVoting
from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.api.websocket.twitchWebsocketEvent import \
    TwitchWebsocketEvent
from CynanBot.twitch.api.websocket.twitchWebsocketSession import \
    TwitchWebsocketSession
from CynanBot.twitch.api.websocket.twitchWebsocketSubscription import \
    TwitchWebsocketSubscription


class TwitchWebsocketJsonMapperInterface(ABC):

    @abstractmethod
    async def parseWebsocketChannelPointsVoting(self, channelPointsVotingJson: Optional[Dict[str, Any]]) -> Optional[TwitchChannelPointsVoting]:
        pass

    @abstractmethod
    async def parseWebsocketPollChoice(self, choiceJson: Optional[Dict[str, Any]]) -> Optional[TwitchPollChoice]:
        pass

    @abstractmethod
    async def parseWebsocketCommunitySubGift(self, giftJson: Optional[Dict[str, Any]]) -> Optional[TwitchCommunitySubGift]:
        pass

    @abstractmethod
    async def parseWebsocketCondition(self, conditionJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketCondition]:
        pass

    @abstractmethod
    async def parseWebsocketDataBundle(self, dataBundleJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketDataBundle]:
        pass

    @abstractmethod
    async def parseWebsocketEvent(self, eventJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketEvent]:
        pass

    @abstractmethod
    async def parseTwitchOutcome(self, outcomeJson: Optional[Dict[str, Any]]) -> Optional[TwitchOutcome]:
        pass

    @abstractmethod
    async def parseTwitchOutcomePredictor(self, predictorJson: Optional[Dict[str, Any]]) -> Optional[TwitchOutcomePredictor]:
        pass

    @abstractmethod
    async def parseWebsocketReward(self, rewardJson: Optional[Dict[str, Any]]) -> Optional[TwitchReward]:
        pass

    @abstractmethod
    async def parseTwitchWebsocketSession(self, sessionJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketSession]:
        pass

    @abstractmethod
    async def parseWebsocketSubGift(self, giftJson: Optional[Dict[str, Any]]) -> Optional[TwitchSubGift]:
        pass

    @abstractmethod
    async def parseWebsocketSubscription(self, subscriptionJson: Optional[Dict[str, Any]]) -> Optional[TwitchWebsocketSubscription]:
        pass
