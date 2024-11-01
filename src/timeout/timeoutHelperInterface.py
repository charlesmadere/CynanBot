from abc import ABC, abstractmethod

from ..twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ..users.userInterface import UserInterface


class TimeoutHelperInterface(ABC):

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass

    @abstractmethod
    async def timeout(
        self,
        bits: int | None,
        durationSeconds: int,
        broadcasterUserId: str,
        chatMessage: str | None,
        instigatorUserId: str,
        instigatorUserName: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        pointRedemptionEventId: str | None,
        pointRedemptionMessage: str | None,
        pointRedemptionRewardId: str | None,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userIdToTimeout: str,
        userNameToTimeout: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        pass
