from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..users.userInterface import UserInterface


class AbsTwitchCheerHandler(ABC):

    @dataclass(frozen = True)
    class CheerData:
        bits: int
        chatMessage: str
        cheerUserId: str
        cheerUserLogin: str
        cheerUserName: str
        twitchChannelId: str
        twitchChatMessageId: str | None
        user: UserInterface

    @abstractmethod
    async def onNewCheer(self, cheerData: CheerData):
        pass

    @abstractmethod
    async def onNewCheerDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
