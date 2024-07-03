from abc import ABC, abstractmethod

from twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from users.userInterface import UserInterface


class AbsTwitchRaidHandler(ABC):

    @abstractmethod
    async def onNewRaid(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
