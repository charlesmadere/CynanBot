from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..users.userInterface import UserInterface


class AbsTwitchFollowHandler(ABC):

    @dataclass(frozen = True)
    class FollowData:
        followedAt: datetime
        followerUserId: str
        followerUserLogin: str
        followerUserName: str
        twitchChannelId: str
        user: UserInterface

    @abstractmethod
    async def onNewFollow(self, followData: FollowData):
        pass

    @abstractmethod
    async def onNewFollowDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass
