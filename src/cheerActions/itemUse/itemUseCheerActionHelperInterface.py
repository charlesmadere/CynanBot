from abc import ABC, abstractmethod

from frozendict import frozendict

from ..absCheerAction import AbsCheerAction
from ...users.userInterface import UserInterface


class ItemUseCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleItemUseCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface,
    ) -> bool:
        pass
