from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..users.userInterface import UserInterface


class AbsTwitchRaidHandler(ABC):

    @dataclass(frozen = True, slots = True)
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
