from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..misc.startable import Startable
from ..users.userInterface import UserInterface


class CheerActionHelperInterface(Startable, ABC):

    @dataclass(frozen = True, slots = True)
    class CheerInfo:
        bits: int
        cheerUserId: str
        cheerUserLogin: str
        cheerUserName: str
        message: str | None
        twitchChannelId: str
        twitchChatMessageId: str | None
        twitchUser: UserInterface

    @abstractmethod
    async def handleCheer(self, cheerInfo: CheerInfo) -> bool:
        pass

    @abstractmethod
    def submitCheer(self, cheerInfo: CheerInfo):
        pass
