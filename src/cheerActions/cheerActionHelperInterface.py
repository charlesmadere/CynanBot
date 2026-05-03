from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..misc.startable import Startable
from ..users.userInterface import UserInterface


class CheerActionHelperInterface(Startable, ABC):

    @dataclass(frozen = True, slots = True)
    class CheerData:
        bits: int
        cheerUserId: str
        cheerUserLogin: str
        cheerUserName: str
        message: str | None
        twitchChannelId: str
        twitchChatMessageId: str | None
        twitchUser: UserInterface

    @abstractmethod
    async def handleCheerAction(
        self,
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str | None,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        user: UserInterface,
    ) -> bool:
        pass

    @abstractmethod
    def submitCheerData(self, cheerData: CheerData):
        pass
