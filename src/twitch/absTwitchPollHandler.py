from abc import ABC, abstractmethod
from dataclasses import dataclass

from frozenlist import FrozenList

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .localModels.twitchPollChoice import TwitchPollChoice
from .localModels.twitchPollStatus import TwitchPollStatus
from ..users.userInterface import UserInterface


class AbsTwitchPollHandler(ABC):

    @dataclass(frozen = True, slots = True)
    class PollData:
        choices: FrozenList[TwitchPollChoice]
        title: str
        twitchChannelId: str
        pollStatus: TwitchPollStatus
        subscriptionType: TwitchWebsocketSubscriptionType
        user: UserInterface

    @abstractmethod
    async def onNewPoll(self, pollData: PollData):
        pass

    @abstractmethod
    async def onNewPollDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
