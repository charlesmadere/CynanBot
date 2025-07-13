from abc import ABC, abstractmethod
from datetime import datetime

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .configuration.twitchChannelProvider import TwitchChannelProvider
from ..users.userInterface import UserInterface


class AbsTwitchFollowHandler(ABC):

    @abstractmethod
    async def onNewFollow(
        self,
        followedAt: datetime,
        followerUserId: str,
        followerUserLogin: str,
        followerUserName: str,
        twitchChannelId: str,
        user: UserInterface,
    ):
        pass

    @abstractmethod
    async def onNewFollowDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
