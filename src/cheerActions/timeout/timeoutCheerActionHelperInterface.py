from abc import ABC, abstractmethod
from typing import Collection

from ..absCheerAction import AbsCheerAction
from ...users.userInterface import UserInterface


class TimeoutCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleTimeoutCheerAction(
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
