from abc import ABC, abstractmethod

from .twitchSubscriptionStatus import TwitchSubscriptionStatus
from ...misc.clearable import Clearable


class TwitchSubscriptionsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def fetchSelfSubscription(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
    ) -> TwitchSubscriptionStatus | None:
        pass

    @abstractmethod
    async def fetchSubscription(
        self,
        chatterUserId: str,
        twitchAccessToken: str,
        twitchChannelId: str,
    ) -> TwitchSubscriptionStatus | None:
        pass

    @abstractmethod
    async def isSubscribed(
        self,
        chatterUserId: str,
        twitchAccessToken: str,
        twitchChannelId: str,
    ) -> bool:
        pass
