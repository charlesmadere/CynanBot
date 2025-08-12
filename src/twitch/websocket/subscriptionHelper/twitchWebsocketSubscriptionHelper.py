import asyncio
import traceback
from typing import Any, Coroutine, Final

from .twitchWebsocketSubscriptionHelperInterface import TwitchWebsocketSubscriptionHelperInterface
from ..conditionBuilder.twitchWebsocketConditionBuilderInterface import TwitchWebsocketConditionBuilderInterface
from ..sessionIdHelper.twitchWebsocketSessionIdHelperInterface import TwitchWebsocketSessionIdHelperInterface
from ..settings.twitchWebsocketSettingsRepositoryInterface import TwitchWebsocketSettingsRepositoryInterface
from ..twitchWebsocketUser import TwitchWebsocketUser
from ...api.models.twitchEventSubRequest import TwitchEventSubRequest
from ...api.models.twitchEventSubResponse import TwitchEventSubResponse
from ...api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ...api.models.twitchWebsocketTransport import TwitchWebsocketTransport
from ...api.models.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod
from ...api.twitchApiServiceInterface import TwitchApiServiceInterface
from ...exceptions import TwitchAccessTokenMissingException
from ...tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class TwitchWebsocketSubscriptionHelper(TwitchWebsocketSubscriptionHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchWebsocketConditionBuilder: TwitchWebsocketConditionBuilderInterface,
        twitchWebsocketSessionIdHelper: TwitchWebsocketSessionIdHelperInterface,
        twitchWebsocketSettingsRepository: TwitchWebsocketSettingsRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchWebsocketConditionBuilder, TwitchWebsocketConditionBuilderInterface):
            raise TypeError(f'twitchWebsocketConditionBuilder argument is malformed: \"{twitchWebsocketConditionBuilder}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchWebsocketSessionIdHelper, TwitchWebsocketSessionIdHelperInterface):
            raise TypeError(f'twitchWebsocketSessionIdHelper argument is malformed: \"{twitchWebsocketSessionIdHelper}\"')
        elif not isinstance(twitchWebsocketSettingsRepository, TwitchWebsocketSettingsRepositoryInterface):
            raise TypeError(f'twitchWebsocketSettingsRepository argument is malformed: \"{twitchWebsocketSettingsRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchWebsocketConditionBuilder: Final[TwitchWebsocketConditionBuilderInterface] = twitchWebsocketConditionBuilder
        self.__twitchWebsocketSessionIdHelper: Final[TwitchWebsocketSessionIdHelperInterface] = twitchWebsocketSessionIdHelper
        self.__twitchWebsocketSettingsRepository: Final[TwitchWebsocketSettingsRepositoryInterface] = twitchWebsocketSettingsRepository

    async def createEventSubSubscriptions(self, user: TwitchWebsocketUser):
        if not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        subscriptionTypes = await self.__twitchWebsocketSettingsRepository.getSubscriptionTypes()

        await self.__createEventSubSubscriptions(
            isFirstSubscriptionAttempt = True,
            subscriptionTypes = subscriptionTypes,
            user = user,
        )

    async def __createEventSubSubscriptions(
        self,
        isFirstSubscriptionAttempt: bool,
        subscriptionTypes: frozenset[TwitchWebsocketSubscriptionType],
        user: TwitchWebsocketUser,
    ):
        if len(subscriptionTypes) == 0:
            self.__timber.log('TwitchWebsocketSubscriptionHelper', f'Skipping creation of EventSub subscriptions as the given set is empty ({user=}) ({subscriptionTypes=})')
            return

        sessionId = self.__twitchWebsocketSessionIdHelper[user]

        if not utils.isValidStr(sessionId):
            self.__timber.log('TwitchWebsocketSubscriptionHelper', f'Skipping creation of {len(subscriptionTypes)} EventSub subscription(s) as this user doesn\'t have a valid session ID ({user=}) ({sessionId=})')
            return

        try:
            userTwitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(user.userId)
        except TwitchAccessTokenMissingException as e:
            self.__timber.log('TwitchWebsocketSubscriptionHelper', f'Skipping creation of {len(subscriptionTypes)} EventSub subscription(s) as we failed to fetch this user\'s Twitch access token ({user=}) ({sessionId=}): {e}', e, traceback.format_exc())
            return

        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = None,
            conduitId = None,
            secret = None,
            sessionId = sessionId,
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
        )

        createEventSubSubscriptionCoroutines: list[Coroutine[TwitchEventSubResponse, Any, Any]] = list()

        for subscriptionType in subscriptionTypes:
            condition = await self.__twitchWebsocketConditionBuilder.build(
                subscriptionType = subscriptionType,
                user = user,
            )

            if condition is None:
                continue

            eventSubRequest = TwitchEventSubRequest(
                twitchChannel = user.userName,
                twitchChannelId = user.userId,
                condition = condition,
                subscriptionType = subscriptionType,
                transport = transport,
            )

            createEventSubSubscriptionCoroutines.append(self.__twitchApiService.createEventSubSubscription(
                twitchAccessToken = userTwitchAccessToken,
                eventSubRequest = eventSubRequest,
            ))

        try:
            await asyncio.gather(*createEventSubSubscriptionCoroutines, return_exceptions = False)
            self.__timber.log('TwitchWebsocketSubscriptionHelper', f'Finished creating {len(subscriptionTypes)} EventSub subscription(s) ({user=}) ({sessionId=})')
        except Exception as e:
            self.__timber.log('TwitchWebsocketSubscriptionHelper', f'Encountered unknown error when creating EventSub subscription(s) ({user=}) ({sessionId=}): {e}', e, traceback.format_exc())

        if isFirstSubscriptionAttempt:
            await self.__inspectEventSubSubscriptionResultsAndMaybeResubscribe(
                requestedSubscriptionTypes = subscriptionTypes,
                userTwitchAccessToken = userTwitchAccessToken,
                user = user,
            )

    async def __inspectEventSubSubscriptionResultsAndMaybeResubscribe(
        self,
        requestedSubscriptionTypes: frozenset[TwitchWebsocketSubscriptionType],
        userTwitchAccessToken: str,
        user: TwitchWebsocketUser,
    ):
        # This method is rather long-winded but what it does is pretty important. We'd
        # prefer using the Twitch CHANNEL_CHAT_MESSAGE EventSub subscription if possible,
        # however, that subscription requires a few more permissions than CHANNEL_CHEER.
        # So what this method intends to do is it will check the list of the successfully
        # created EventSub subscriptions, and if CHANNEL_CHAT_MESSAGE was requested, but
        # failed, and CHANNEL_CHEER was NOT requested, then we will create a CHANNEL_CHEER
        # subscription.

        if not await self.__twitchWebsocketSettingsRepository.isChatEventToCheerEventSubscriptionFallbackEnabled():
            return
        elif len(requestedSubscriptionTypes) == 0:
            return
        elif TwitchWebsocketSubscriptionType.CHANNEL_BITS_USE not in requestedSubscriptionTypes:
            return
        elif TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE not in requestedSubscriptionTypes:
            return
        elif TwitchWebsocketSubscriptionType.CHANNEL_CHEER in requestedSubscriptionTypes:
            return

        # Sleep a little bit before making the following API call, just to ensure things are
        # finished being initialized/configured on Twitch's end.
        await asyncio.sleep(1)

        try:
            eventSubSubscriptions = await self.__twitchApiService.fetchEventSubSubscriptions(
                twitchAccessToken = userTwitchAccessToken,
                userId = user.userId,
            )
        except Exception as e:
            self.__timber.log('TwitchWebsocketSubscriptionHelper', f'Failed to fetch EventSub subscriptions ({user=}): {e}', e, traceback.format_exc())
            return

        successfulSubscriptionTypes: set[TwitchWebsocketSubscriptionType] = set()

        for result in eventSubSubscriptions.data:
            successfulSubscriptionTypes.add(result.subscriptionType)

        if TwitchWebsocketSubscriptionType.CHANNEL_BITS_USE in successfulSubscriptionTypes:
            return
        elif TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE in successfulSubscriptionTypes:
            return
        elif TwitchWebsocketSubscriptionType.CHANNEL_CHEER in successfulSubscriptionTypes:
            return

        self.__timber.log('TwitchWebsocketSubscriptionHelper', f'It looks like we failed to create a chat message EventSub subscription, so let\'s fallback to creating a cheer EventSub subscription instead ({user=}) ({successfulSubscriptionTypes=})')

        await self.__createEventSubSubscriptions(
            isFirstSubscriptionAttempt = False,
            subscriptionTypes = frozenset({ TwitchWebsocketSubscriptionType.CHANNEL_CHEER }),
            user = user,
        )
