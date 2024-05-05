from abc import ABC, abstractmethod
from typing import Any

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
    async def parseWebsocketChannelPointsVoting(
        self,
        channelPointsVotingJson: dict[str, Any] | None
    ) -> TwitchChannelPointsVoting | None:
        pass

    @abstractmethod
    async def parseWebsocketPollChoice(
        self,
        choiceJson: dict[str, Any] | None
    ) -> TwitchPollChoice | None:
        pass

    @abstractmethod
    async def parseWebsocketCommunitySubGift(
        self,
        giftJson: dict[str, Any] | None
    ) -> TwitchCommunitySubGift | None:
        pass

    @abstractmethod
    async def parseWebsocketCondition(
        self,
        conditionJson: dict[str, Any] | None
    ) -> TwitchWebsocketCondition | None:
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
    async def parseTwitchOutcomePredictor(
        self,
        predictorJson: dict[str, Any] | None
    ) -> TwitchOutcomePredictor | None:
        pass

    @abstractmethod
    async def parseWebsocketReward(
        self,
        rewardJson: dict[str, Any] | None
    ) -> TwitchReward | None:
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
