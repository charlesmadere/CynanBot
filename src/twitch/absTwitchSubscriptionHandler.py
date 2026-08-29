from abc import ABC, abstractmethod
from dataclasses import dataclass

from .api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from .api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .localModels.twitchCommunitySubGift import TwitchCommunitySubGift
from .localModels.twitchResub import TwitchResub
from .localModels.twitchResubscriptionMessage import TwitchResubscriptionMessage
from .localModels.twitchSubGift import TwitchSubGift
from .localModels.twitchSubscriberTier import TwitchSubscriberTier
from ..users.userInterface import UserInterface


class AbsTwitchSubscriptionHandler(ABC):

    @dataclass(frozen = True, slots = True)
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
