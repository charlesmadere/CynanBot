from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .configuration.twitchChannelProvider import TwitchChannelProvider
from ..users.userInterface import UserInterface


class AbsTwitchRaidHandler(ABC):

    @dataclass(frozen = True)
    class RaidData:
        viewers: int
        raidUserId: str
        raidUserLogin: str
        raidUserName: str
        twitchChannelId: str
        user: UserInterface

    @abstractmethod
    async def onNewRaid(self, raidData: RaidData):
        pass

    @abstractmethod
    async def onNewRaidDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
