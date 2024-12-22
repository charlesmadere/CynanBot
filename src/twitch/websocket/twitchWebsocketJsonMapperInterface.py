from abc import ABC, abstractmethod
from typing import Any

from ..api.twitchCommunitySubGift import TwitchCommunitySubGift
from ..api.twitchOutcome import TwitchOutcome
from ..api.twitchOutcomePredictor import TwitchOutcomePredictor
from ..api.twitchPollChoice import TwitchPollChoice
from ..api.twitchResub import TwitchResub
from ..api.twitchReward import TwitchReward
from ..api.twitchSubGift import TwitchSubGift
from ..api.websocket.twitchWebsocketChannelPointsVoting import TwitchWebsocketChannelPointsVoting
from ..api.websocket.twitchWebsocketCondition import TwitchWebsocketCondition
from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.websocket.twitchWebsocketEvent import TwitchWebsocketEvent
from ..api.websocket.twitchWebsocketMessageType import TwitchWebsocketMessageType
from ..api.websocket.twitchWebsocketSession import TwitchWebsocketSession
from ..api.websocket.twitchWebsocketSubscription import TwitchWebsocketSubscription
from ..api.websocket.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod


class TwitchWebsocketJsonMapperInterface(ABC):

    @abstractmethod
    async def parseTransportMethod(
        self,
        transportMethod: str | Any | None
    ) -> TwitchWebsocketTransportMethod | None:
        pass

    @abstractmethod
    async def parseWebsocketChannelPointsVoting(
        self,
        channelPointsVotingJson: dict[str, Any] | None
    ) -> TwitchWebsocketChannelPointsVoting | None:
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
        giftJson: dict[str, Any] | Any | None
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
    async def parseWebsocketMessageType(
        self,
        messageType: str | Any | None
    ) -> TwitchWebsocketMessageType | None:
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
        predictorJson: dict[str, Any] | Any | None
    ) -> TwitchOutcomePredictor | None:
        pass

    @abstractmethod
    async def parseWebsocketResub(
        self,
        resubJson: dict[str, Any] | None
    ) -> TwitchResub | None:
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

    @abstractmethod
    async def requireTransportMethod(
        self,
        transportMethod: str | Any | None
    ) -> TwitchWebsocketTransportMethod:
        pass

    @abstractmethod
    async def requireWebsocketMessageType(
        self,
        messageType: str | Any | None
    ) -> TwitchWebsocketMessageType:
        pass
