from abc import abstractmethod

from .twitchSubscriptionStatus import TwitchSubscriptionStatus
from ...misc.clearable import Clearable


class TwitchSubscriptionsRepositoryInterface(Clearable):

    @abstractmethod
    async def fetchBroadcasterSubscription(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> TwitchSubscriptionStatus | None:
        pass

    @abstractmethod
    async def fetchSubscriptionStatus(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> TwitchSubscriptionStatus | None:
        pass

    @abstractmethod
    async def isSubscribed(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> bool:
        pass
