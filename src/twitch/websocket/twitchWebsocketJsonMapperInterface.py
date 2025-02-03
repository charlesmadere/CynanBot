from abc import ABC, abstractmethod
from typing import Any

from ..api.models.twitchCommunitySubGift import TwitchCommunitySubGift
from ..api.models.twitchOutcome import TwitchOutcome
from ..api.models.twitchOutcomePredictor import TwitchOutcomePredictor
from ..api.models.twitchPollChoice import TwitchPollChoice
from ..api.models.twitchSubGift import TwitchSubGift
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketEvent import TwitchWebsocketEvent
from ..api.models.twitchWebsocketSession import TwitchWebsocketSession
from ..api.models.twitchWebsocketSubscription import TwitchWebsocketSubscription


class TwitchWebsocketJsonMapperInterface(ABC):

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
        predictorJson: dict[str, Any] | Any | None
    ) -> TwitchOutcomePredictor | None:
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
