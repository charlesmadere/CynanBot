from __future__ import annotations

import traceback
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta

from lru import LRU

from .twitchSubscriptionStatus import TwitchSubscriptionStatus
from .twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface
from ..api.models.twitchUserSubscription import TwitchUserSubscription
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..exceptions import TwitchJsonException, TwitchStatusCodeException
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


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
        cacheSize: int = 64,
        cacheTimeToLive: timedelta = timedelta(hours = 3)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not utils.isValidInt(cacheSize):
            raise TypeError(f'cacheSize argument is malformed: \"{cacheSize}\"')
        elif cacheSize < 1 or cacheSize > utils.getIntMaxSafeSize():
            raise ValueError(f'cacheSize argument is out of bounds: {cacheSize}')
        elif not isinstance(cacheTimeToLive, timedelta):
            raise TypeError(f'cacheTimeToLive argument is malformed: \"{cacheTimeToLive}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__cacheTimeToLive: timedelta = cacheTimeToLive

        self.__caches: dict[str, LRU[str, TwitchSubscriptionsRepository.Entry | None]] = defaultdict(lambda: LRU(cacheSize))

    async def clearCaches(self):
        self.__caches.clear()
        self.__timber.log('TwitchSubscriptionsRepository', 'Caches cleared')

    async def fetchSubscriptionStatus(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> TwitchSubscriptionStatus | None:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        subscriptionEntry = self.__caches[twitchChannelId].get(userId, None)
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if subscriptionEntry is not None and subscriptionEntry.fetchTime + self.__cacheTimeToLive >= now:
            return subscriptionEntry.subscriptionStatus

        userSubscription = await self.__fetchFromTwitchApi(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = userId
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
            userId = userId,
            tier = userSubscription.tier
        )

        self.__caches[twitchChannelId][userId] = TwitchSubscriptionsRepository.Entry(
            fetchTime = now,
            subscriptionStatus = subscriptionStatus
        )

        return subscriptionStatus

    async def __fetchFromTwitchApi(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> TwitchUserSubscription | None:
        try:
            return await self.__twitchApiService.fetchUserSubscription(
                broadcasterId = twitchChannelId,
                chatterUserId = userId,
                twitchAccessToken = twitchAccessToken
            )
        except (GenericNetworkException, TwitchJsonException, TwitchStatusCodeException) as e:
            self.__timber.log('TwitchSubscriptionsRepository', f'Failed to fetch Twitch subscription status from Twitch API ({twitchAccessToken=}) ({twitchChannelId=}) ({userId=}): {e}', e, traceback.format_exc())
            return None

    async def isSubscribed(
        self,
        twitchAccessToken: str,
        twitchChannelId: str,
        userId: str
    ) -> bool:
        if not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        subscriptionStatus = await self.fetchSubscriptionStatus(
            twitchAccessToken = twitchAccessToken,
            twitchChannelId = twitchChannelId,
            userId = userId
        )

        return subscriptionStatus is not None
