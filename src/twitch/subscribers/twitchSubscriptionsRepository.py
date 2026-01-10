from __future__ import annotations

import traceback
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final

from lru import LRU

from .twitchSubscriptionStatus import TwitchSubscriptionStatus
from .twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface
from ..api.models.twitchBroadcasterSubscription import TwitchBroadcasterSubscription
from ..api.models.twitchUserSubscription import TwitchUserSubscription
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..exceptions import TwitchJsonException, TwitchStatusCodeException
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchSubscriptionsRepository(TwitchSubscriptionsRepositoryInterface):

    @dataclass(frozen = True)
    class Entry:
        fetchTime: datetime
        subscriptionStatus: TwitchSubscriptionStatus

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        cacheSize: int = 64,
        cacheTimeToLive: timedelta = timedelta(hours = 3),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')
        elif not isinstance(cacheTimeToLive, timedelta):
            raise TypeError(f'cacheTimeToLive argument is malformed: \"{cacheTimeToLive}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__cacheTimeToLive: Final[timedelta] = cacheTimeToLive

        self.__chatterCaches: Final[dict[str, LRU[str, TwitchSubscriptionsRepository.Entry | None]]] = defaultdict(lambda: LRU(cacheSize))
        self.__selfCaches: Final[LRU[str, TwitchSubscriptionsRepository.Entry | None]] = LRU(cacheSize)

    async def clearCaches(self):
        self.__chatterCaches.clear()
        self.__selfCaches.clear()
        self.__timber.log('TwitchSubscriptionsRepository', 'Caches cleared')

    async def fetchSelfSubscription(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
    ) -> TwitchSubscriptionStatus | None:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        subscriptionEntry = self.__selfCaches.get(twitchChannelId, None)
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if subscriptionEntry is not None and subscriptionEntry.fetchTime + self.__cacheTimeToLive >= now:
            return subscriptionEntry.subscriptionStatus

        selfUserId = await self.__userIdsRepository.requireUserId(
            userName = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchAccessToken = twitchAccessToken,
        )

        userSubscription = await self.__fetchSelfSubscriptionFromTwitch(
            selfUserId = selfUserId,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
        )

        if userSubscription is None:
            return None

        subscriptionStatus = TwitchSubscriptionStatus(
            isGift = userSubscription.isGift,
            broadcasterId = userSubscription.broadcasterId,
            broadcasterLogin = userSubscription.broadcasterLogin,
            broadcasterName = userSubscription.broadcasterName,
            gifterId = userSubscription.gifterId,
            gifterLogin = userSubscription.gifterLogin,
            gifterName = userSubscription.gifterName,
            userId = selfUserId,
            tier = userSubscription.tier,
        )

        self.__selfCaches[twitchChannelId] = TwitchSubscriptionsRepository.Entry(
            fetchTime = now,
            subscriptionStatus = subscriptionStatus,
        )

        return subscriptionStatus

    async def __fetchSelfSubscriptionFromTwitch(
        self,
        selfUserId: str,
        twitchAccessToken: str,
        twitchChannelId: str,
    ) -> TwitchUserSubscription | None:
        try:
            return await self.__twitchApiService.checkUserSubscription(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchAccessToken,
                userId = selfUserId,
            )
        except (GenericNetworkException, TwitchJsonException, TwitchStatusCodeException) as e:
            self.__timber.log('TwitchSubscriptionsRepository', f'Failed to fetch self subscription from Twitch API ({selfUserId=}) ({twitchChannelId=})', e, traceback.format_exc())
            return None

    async def fetchSubscription(
        self,
        chatterUserId: str,
        twitchAccessToken: str,
        twitchChannelId: str,
    ) -> TwitchSubscriptionStatus | None:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        subscriptionEntry = self.__chatterCaches[twitchChannelId].get(chatterUserId, None)
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if subscriptionEntry is not None and subscriptionEntry.fetchTime + self.__cacheTimeToLive >= now:
            return subscriptionEntry.subscriptionStatus

        broadcasterSubscription = await self.__fetchSubscriptionFromTwitch(
            chatterUserId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
        )

        if broadcasterSubscription is None:
            return None

        subscriptionStatus = TwitchSubscriptionStatus(
            isGift = broadcasterSubscription.isGift,
            broadcasterId = broadcasterSubscription.broadcasterId,
            broadcasterLogin = broadcasterSubscription.broadcasterLogin,
            broadcasterName = broadcasterSubscription.broadcasterName,
            gifterId = broadcasterSubscription.gifterId,
            gifterLogin = broadcasterSubscription.gifterLogin,
            gifterName = broadcasterSubscription.gifterName,
            userId = chatterUserId,
            tier = broadcasterSubscription.tier,
        )

        self.__chatterCaches[twitchChannelId][chatterUserId] = TwitchSubscriptionsRepository.Entry(
            fetchTime = now,
            subscriptionStatus = subscriptionStatus,
        )

        return subscriptionStatus

    async def __fetchSubscriptionFromTwitch(
        self,
        chatterUserId: str,
        twitchAccessToken: str,
        twitchChannelId: str,
    ) -> TwitchBroadcasterSubscription | None:
        try:
            broadcasterSubscriptionsResponse = await self.__twitchApiService.fetchBroadcasterSubscriptions(
                broadcasterId = twitchChannelId,
                twitchAccessToken = twitchAccessToken,
                userId = chatterUserId,
            )
        except (GenericNetworkException, TwitchJsonException, TwitchStatusCodeException) as e:
            self.__timber.log('TwitchSubscriptionsRepository', f'Failed to fetch subscription from Twitch API ({chatterUserId=}) ({twitchChannelId=})', e, traceback.format_exc())
            return None

        for broadcasterSubscription in broadcasterSubscriptionsResponse.data:
            if broadcasterSubscription.userId == chatterUserId:
                return broadcasterSubscription

        return None

    async def isSubscribed(
        self,
        chatterUserId: str,
        twitchAccessToken: str,
        twitchChannelId: str,
    ) -> bool:
        if not utils.isValidStr(chatterUserId):
            raise TypeError(f'chatterUserId argument is malformed: \"{chatterUserId}\"')
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        subscriptionStatus = await self.fetchSubscription(
            chatterUserId = chatterUserId,
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
        )

        return subscriptionStatus is not None
