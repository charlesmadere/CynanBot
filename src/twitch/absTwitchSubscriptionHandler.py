from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchCommunitySubGift import TwitchCommunitySubGift
from .api.models.twitchResub import TwitchResub
from .api.models.twitchResubscriptionMessage import TwitchResubscriptionMessage
from .api.models.twitchSubGift import TwitchSubGift
from .api.models.twitchSubscriberTier import TwitchSubscriberTier
from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .configuration.twitchChannelProvider import TwitchChannelProvider
from ..users.userInterface import UserInterface


class AbsTwitchSubscriptionHandler(ABC):

    @dataclass(frozen = True)
    class SubscriptionData:
        isAnonymous: bool | None
        isGift: bool | None
        total: int | None
        chatMessage: str | None
        eventUserId: str
        eventUserLogin: str
        eventUserName: str
        twitchChannelId: str
        communitySubGift: TwitchCommunitySubGift | None
        resub: TwitchResub | None
        resubscriptionMessage: TwitchResubscriptionMessage | None
        subGift: TwitchSubGift | None
        tier: TwitchSubscriberTier
        subscriptionType: TwitchWebsocketSubscriptionType
        user: UserInterface

    @abstractmethod
    async def onNewSubscription(self, subscriptionData: SubscriptionData):
        pass

    @abstractmethod
    async def onNewSubscriptionDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        pass

    @abstractmethod
    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        pass
