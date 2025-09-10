from abc import ABC, abstractmethod

from frozendict import frozendict

from ..absCheerAction import AbsCheerAction
from ...users.userInterface import UserInterface


class VoicemailCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleVoicemailCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface,
    ) -> bool:
        pass
