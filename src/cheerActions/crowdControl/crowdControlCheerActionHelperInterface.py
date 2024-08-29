from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..absCheerAction import AbsCheerAction
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...users.userInterface import UserInterface


class CrowdControlCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleCrowdControlCheerAction(
        self,
        actions: FrozenList[AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
