from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..users.userInterface import UserInterface


class AbsTwitchChannelPointRedemptionHandler(ABC):

    @dataclass(frozen = True)
    class AnnouncementData:
        announcementMessage: str
        announcementUserId: str
        announcementUserLogin: str
        announcementUserName: str
        twitchChannelId: str
        user: UserInterface

    @abstractmethod
    async def onNewAnnouncement(self, announcementData: AnnouncementData):
        pass

    @abstractmethod
    async def onNewAnnouncementDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
