from abc import ABC, abstractmethod
from typing import Collection

from ..absCheerAction import AbsCheerAction
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...users.userInterface import UserInterface


class BeanChanceCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleBeanChanceCheerAction(
        self,
        actions: Collection[AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
