from abc import ABC, abstractmethod

from frozendict import frozendict

from ..absCheerAction import AbsCheerAction
from ...users.userInterface import UserInterface


class TtsCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleTtsCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str | None,
        twitchChannelId: str,
        twitchUser: UserInterface,
    ) -> bool:
        pass
