from abc import ABC, abstractmethod
from dataclasses import dataclass

from frozenlist import FrozenList

from .api.models.twitchOutcome import TwitchOutcome
from .api.models.twitchPredictionStatus import TwitchPredictionStatus
from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..users.userInterface import UserInterface


class AbsTwitchPredictionHandler(ABC):

    @dataclass(frozen = True)
    class PredictionData:
        outcomes: FrozenList[TwitchOutcome]
        eventId: str
        title: str
        twitchChannelId: str
        winningOutcomeId: str | None
        predictionStatus: TwitchPredictionStatus | None
        subscriptionType: TwitchWebsocketSubscriptionType
        user: UserInterface

    @abstractmethod
    async def onNewPrediction(self, predictionData: PredictionData):
        pass

    @abstractmethod
    async def onNewPredictionDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
