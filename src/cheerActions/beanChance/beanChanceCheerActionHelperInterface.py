from abc import ABC, abstractmethod

from ..absCheerAction import AbsCheerAction
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...users.userInterface import UserInterface


class BeanChanceCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleTimeoutCheerAction(
        self,
        bits: int,
        actions: list[AbsCheerAction],
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
