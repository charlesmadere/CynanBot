from abc import ABC, abstractmethod

from frozendict import frozendict

from ..absCheerAction import AbsCheerAction
from ...users.userInterface import UserInterface


class TimeoutCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleTimeoutCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
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
