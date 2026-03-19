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
            self.__timber.log('TwitchWebsocketSubscriptionHelper', f'Skipping creation of {len(subscriptionTypes)} EventSub subscription(s) as we failed to fetch this user\'s Twitch access token ({user=}) ({sessionId=})', e, traceback.format_exc())
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
            self.__timber.log('TwitchWebsocketSubscriptionHelper', f'Encountered unknown error when creating EventSub subscription(s) ({user=}) ({sessionId=})', e, traceback.format_exc())
