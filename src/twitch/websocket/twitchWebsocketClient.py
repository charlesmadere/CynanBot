import asyncio
import json
import queue
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue
from typing import Any, Coroutine

import websockets

from .conditionBuilder.twitchWebsocketConditionBuilderInterface import TwitchWebsocketConditionBuilderInterface
from .connectionAction.twitchWebsocketConnectionAction import TwitchWebsocketConnectionAction
from .connectionAction.twitchWebsocketConnectionActionHelperInterface import \
    TwitchWebsocketConnectionActionHelperInterface
from .endpointHelper.twitchWebsocketEndpointHelperInterface import TwitchWebsocketEndpointHelperInterface
from .instabilityHelper.twitchWebsocketInstabilityHelperInterface import TwitchWebsocketInstabilityHelperInterface
from .listener.twitchWebsocketDataBundleListener import TwitchWebsocketDataBundleListener
from .sessionIdHelper.twitchWebsocketSessionIdHelperInterface import TwitchWebsocketSessionIdHelperInterface
from .settings.twitchWebsocketSettingsRepositoryInterface import TwitchWebsocketSettingsRepositoryInterface
from .twitchWebsocketAllowedUsersRepositoryInterface import TwitchWebsocketAllowedUsersRepositoryInterface
from .twitchWebsocketClientInterface import TwitchWebsocketClientInterface
from .twitchWebsocketJsonLoggingLevel import TwitchWebsocketJsonLoggingLevel
from .twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from .twitchWebsocketUser import TwitchWebsocketUser
from ..api.models.twitchEventSubRequest import TwitchEventSubRequest
from ..api.models.twitchEventSubResponse import TwitchEventSubResponse
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketMessageType import TwitchWebsocketMessageType
from ..api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..api.models.twitchWebsocketTransport import TwitchWebsocketTransport
from ..api.models.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod
from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...misc.lruCache import LruCache
from ...timber.timberInterface import TimberInterface


class TwitchWebsocketClient(TwitchWebsocketClientInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchWebsocketAllowedUsersRepository: TwitchWebsocketAllowedUsersRepositoryInterface,
        twitchWebsocketConditionBuilder: TwitchWebsocketConditionBuilderInterface,
        twitchWebsocketConnectionActionHelper: TwitchWebsocketConnectionActionHelperInterface,
        twitchWebsocketEndpointHelper: TwitchWebsocketEndpointHelperInterface,
        twitchWebsocketInstabilityHelper: TwitchWebsocketInstabilityHelperInterface,
        twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface,
        twitchWebsocketSessionIdHelper: TwitchWebsocketSessionIdHelperInterface,
        twitchWebsocketSettingsRepository: TwitchWebsocketSettingsRepositoryInterface,
        queueSleepTimeSeconds: float = 1,
        queueTimeoutSeconds: float = 3,
        websocketCreationDelayTimeSeconds: float = 0.5,
        websocketRetrySleepTimeSeconds: float = 3,
        subscriptionTypes: frozenset[TwitchWebsocketSubscriptionType] = frozenset({
            TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE,
            TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_END,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS,
            TwitchWebsocketSubscriptionType.CHEER,
            TwitchWebsocketSubscriptionType.FOLLOW,
            TwitchWebsocketSubscriptionType.RAID,
            TwitchWebsocketSubscriptionType.SUBSCRIBE,
            TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT,
            TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
        }),
        twitchWebsocketInstabilityThreshold: int = 3,
        maxMessageAge: timedelta = timedelta(minutes = 1, seconds = 30)
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchWebsocketAllowedUsersRepository, TwitchWebsocketAllowedUsersRepositoryInterface):
            raise TypeError(f'twitchWebsocketAllowedUsersRepository argument is malformed: \"{twitchWebsocketAllowedUsersRepository}\"')
        elif not isinstance(twitchWebsocketConditionBuilder, TwitchWebsocketConditionBuilderInterface):
            raise TypeError(f'twitchWebsocketConditionBuilder argument is malformed: \"{twitchWebsocketConditionBuilder}\"')
        elif not isinstance(twitchWebsocketConnectionActionHelper, TwitchWebsocketConnectionActionHelperInterface):
            raise TypeError(f'twitchWebsocketConnectionActionHelper argument is malformed: \"{twitchWebsocketConnectionActionHelper}\"')
        elif not isinstance(twitchWebsocketEndpointHelper, TwitchWebsocketEndpointHelperInterface):
            raise TypeError(f'twitchWebsocketEndpointHelper argument is malformed: \"{twitchWebsocketEndpointHelper}\"')
        elif not isinstance(twitchWebsocketInstabilityHelper, TwitchWebsocketInstabilityHelperInterface):
            raise TypeError(f'twitchWebsocketInstabilityHelper argument is malformed: \"{twitchWebsocketInstabilityHelper}\"')
        elif not isinstance(twitchWebsocketJsonMapper, TwitchWebsocketJsonMapperInterface):
            raise TypeError(f'twitchWebsocketJsonMapper argument is malformed: \"{twitchWebsocketJsonMapper}\"')
        elif not isinstance(twitchWebsocketSessionIdHelper, TwitchWebsocketSessionIdHelperInterface):
            raise TypeError(f'twitchWebsocketSessionIdHelper argument is malformed: \"{twitchWebsocketSessionIdHelper}\"')
        elif not isinstance(twitchWebsocketSettingsRepository, TwitchWebsocketSettingsRepositoryInterface):
            raise TypeError(f'twitchWebsocketSettingsRepository argument is malformed: \"{twitchWebsocketSettingsRepository}\"')
        elif not utils.isValidNum(queueSleepTimeSeconds):
            raise TypeError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 15:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')
        elif not utils.isValidNum(websocketCreationDelayTimeSeconds):
            raise TypeError(f'websocketCreationDelayTimeSeconds argument is malformed: \"{websocketCreationDelayTimeSeconds}\"')
        elif websocketCreationDelayTimeSeconds < 0.1 or websocketCreationDelayTimeSeconds > 8:
            raise ValueError(f'websocketCreationDelayTimeSeconds argument is out of bounds: {websocketCreationDelayTimeSeconds}')
        elif not utils.isValidNum(websocketRetrySleepTimeSeconds):
            raise TypeError(f'websocketRetrySleepTimeSeconds argument is malformed: \"{websocketRetrySleepTimeSeconds}\"')
        elif websocketRetrySleepTimeSeconds < 1 or websocketRetrySleepTimeSeconds > 8:
            raise ValueError(f'websocketRetrySleepTimeSeconds argument is out of bounds: {websocketRetrySleepTimeSeconds}')
        elif not isinstance(subscriptionTypes, frozenset):
            raise TypeError(f'subscriptionTypes argument is malformed: \"{subscriptionTypes}\"')
        elif not utils.isValidInt(twitchWebsocketInstabilityThreshold):
            raise TypeError(f'twitchWebsocketInstabilityThreshold argument is malformed: \"{twitchWebsocketInstabilityThreshold}\"')
        elif twitchWebsocketInstabilityThreshold < 1 or twitchWebsocketInstabilityThreshold > 8:
            raise ValueError(f'twitchWebsocketInstabilityThreshold argument is out of bounds: {twitchWebsocketInstabilityThreshold}')
        elif not isinstance(maxMessageAge, timedelta):
            raise TypeError(f'maxMessageAge argument is malformed: \"{maxMessageAge}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchWebsocketAllowedUsersRepository: TwitchWebsocketAllowedUsersRepositoryInterface = twitchWebsocketAllowedUsersRepository
        self.__twitchWebsocketConditionBuilder: TwitchWebsocketConditionBuilderInterface = twitchWebsocketConditionBuilder
        self.__twitchWebsocketConnectionActionHelper: TwitchWebsocketConnectionActionHelperInterface = twitchWebsocketConnectionActionHelper
        self.__twitchWebsocketEndpointHelper: TwitchWebsocketEndpointHelperInterface = twitchWebsocketEndpointHelper
        self.__twitchWebsocketInstabilityHelper: TwitchWebsocketInstabilityHelperInterface = twitchWebsocketInstabilityHelper
        self.__twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = twitchWebsocketJsonMapper
        self.__twitchWebsocketSessionIdHelper: TwitchWebsocketSessionIdHelperInterface = twitchWebsocketSessionIdHelper
        self.__twitchWebsocketSettingsRepository: TwitchWebsocketSettingsRepositoryInterface = twitchWebsocketSettingsRepository
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__queueTimeoutSeconds: float = queueTimeoutSeconds
        self.__websocketCreationDelayTimeSeconds: float = websocketCreationDelayTimeSeconds
        self.__websocketRetrySleepTimeSeconds: float = websocketRetrySleepTimeSeconds
        self.__subscriptionTypes: frozenset[TwitchWebsocketSubscriptionType] = subscriptionTypes
        self.__twitchWebsocketInstabilityThreshold: int = twitchWebsocketInstabilityThreshold
        self.__maxMessageAge: timedelta = maxMessageAge

        self.__isStarted: bool = False
        self.__messageIdCache: LruCache = LruCache(128)
        self.__dataBundleQueue: SimpleQueue[TwitchWebsocketDataBundle] = SimpleQueue()
        self.__dataBundleListener: TwitchWebsocketDataBundleListener | None = None

    async def __createEventSubSubscription(self, user: TwitchWebsocketUser):
        if not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        sessionId = self.__twitchWebsocketSessionIdHelper[user]

        if not utils.isValidStr(sessionId):
            self.__timber.log('TwitchWebsocketClient', f'Skipping creation of EventSub subscription(s) ({user=}) ({sessionId=})')
            return

        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            conduitId = None,
            secret = None,
            sessionId = sessionId,
            method = TwitchWebsocketTransportMethod.WEBSOCKET
        )

        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(user.userId)
        createEventSubScriptionCoroutines: list[Coroutine[TwitchEventSubResponse, Any, Any]] = list()

        for subscriptionType in self.__subscriptionTypes:
            condition = await self.__twitchWebsocketConditionBuilder.build(
                subscriptionType = subscriptionType,
                user = user
            )

            if condition is None:
                continue

            eventSubRequest = TwitchEventSubRequest(
                condition = condition,
                subscriptionType = subscriptionType,
                transport = transport
            )

            createEventSubScriptionCoroutines.append(self.__twitchApiService.createEventSubSubscription(
                twitchAccessToken = twitchAccessToken,
                eventSubRequest = eventSubRequest
            ))

        try:
            await asyncio.gather(*createEventSubScriptionCoroutines, return_exceptions = True)
            self.__timber.log('TwitchWebsocketClient', f'Finished creating EventSub subscription(s) ({user=}) ({sessionId=})')
        except Exception as e:
            self.__timber.log('TwitchWebsocketClient', f'Encountered unknown error when creating EventSub subscription(s) ({user=}) ({sessionId=}): {e}', e, traceback.format_exc())

    async def __isValidDataBundle(self, dataBundle: TwitchWebsocketDataBundle) -> bool:
        if not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        # ensure that this isn't a message we've seen before
        if self.__messageIdCache.contains(dataBundle.metadata.messageId):
            self.__timber.log('TwitchWebsocketClient', f'Encountered a message that has already been seen ({dataBundle.metadata.messageId=}) ({dataBundle=})')
            return False

        self.__messageIdCache.put(dataBundle.metadata.messageId)

        # ensure that this message isn't gratuitously old
        messageTimestamp = dataBundle.metadata.messageTimestamp
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if now - messageTimestamp >= self.__maxMessageAge:
            self.__timber.log('TwitchWebsocketClient', f'Encountered a message that is too old ({dataBundle.metadata.messageId=}) ({dataBundle=})')
            return False

        return True

    async def __logWebsocketMessage(
        self,
        message: str,
        dataBundle: TwitchWebsocketDataBundle | None,
        user: TwitchWebsocketUser
    ):
        if not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        jsonLoggingLevel = await self.__twitchWebsocketSettingsRepository.getLoggingLevel()
        shouldLog = False

        if jsonLoggingLevel is TwitchWebsocketJsonLoggingLevel.ALL:
            shouldLog = True
        elif dataBundle is None:
            shouldLog = True
        elif jsonLoggingLevel is TwitchWebsocketJsonLoggingLevel.LIMITED and dataBundle.metadata.messageType is not TwitchWebsocketMessageType.KEEP_ALIVE:
            shouldLog = True

        if not shouldLog or jsonLoggingLevel is TwitchWebsocketJsonLoggingLevel.NONE:
            return

        self.__timber.log('TwitchWebsocketClient', f'Websocket message: ({user=}) ({message=}) ({dataBundle=})')

    async def __parseMessageToDataBundleFor(
        self,
        message: str | Any | None,
        user: TwitchWebsocketUser
    ) -> TwitchWebsocketDataBundle | None:
        if not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if message is None:
            self.__timber.log('TwitchWebsocketClient', f'Received a None message instance: ({message=}) ({user=})')
            return None
        elif not isinstance(message, str):
            self.__timber.log('TwitchWebsocketClient', f'Received a message instance that is of an unexpected type: ({message=}) ({user=})')
            return None
        elif not utils.isValidStr(message):
            self.__timber.log('TwitchWebsocketClient', f'Received an empty/blank message String: ({message=}) ({user=})')
            return None

        dictionary: dict[str, Any] | Any | None

        try:
            dictionary = json.loads(message)
        except Exception as e:
            self.__timber.log('TwitchWebsocketClient', f'Encountered an exception when attempting to parse message into JSON dictionary ({message=}) ({user=}): {e}', e, traceback.format_exc())
            return None

        if not isinstance(dictionary, dict) or len(dictionary) == 0:
            self.__timber.log('TwitchWebsocketClient', f'Message was parsed into an unexpected or malformed type ({dictionary=}) ({message=}) ({user=})')
            return None

        dataBundle: TwitchWebsocketDataBundle | None = None
        exception: Exception | None = None

        try:
            dataBundle = await self.__twitchWebsocketJsonMapper.parseWebsocketDataBundle(dictionary)
        except Exception as e:
            exception = e

        await self.__logWebsocketMessage(
            message = message,
            dataBundle = dataBundle,
            user = user
        )

        if exception is not None:
            self.__timber.log('TwitchWebsocketClient', f'Encountered an exception when attempting to convert dictionary into TwitchWebsocketDataBundle ({dataBundle=}) ({dictionary=}) ({message=}) ({user=}): {exception}', exception, traceback.format_exc())
            return None
        elif dataBundle is None:
            self.__timber.log('TwitchWebsocketClient', f'Received `None` when attempting to convert dictionary into TwitchWebsocketDataBundle ({dataBundle=}) ({dictionary=}) ({message=}) ({user=})')
            return None
        else:
            return dataBundle

    def setDataBundleListener(self, listener: TwitchWebsocketDataBundleListener | None):
        if listener is not None and not isinstance(listener, TwitchWebsocketDataBundleListener):
            raise TypeError(f'listener argument is malformed: \"{listener}\"')

        self.__dataBundleListener = listener

    def start(self):
        if self.__isStarted:
            self.__timber.log('TwitchWebsocketClient', 'Not starting TwitchWebsocketClient as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('TwitchWebsocketClient', 'Starting TwitchWebsocketClient...')
        self.__backgroundTaskHelper.createTask(self.__startWebsocketConnections())
        self.__backgroundTaskHelper.createTask(self.__startDataBundleLoop())

    async def __startDataBundleLoop(self):
        while True:
            dataBundleListener = self.__dataBundleListener

            if dataBundleListener is not None:
                dataBundles: list[TwitchWebsocketDataBundle] = list()

                try:
                    while not self.__dataBundleQueue.empty():
                        dataBundles.append(self.__dataBundleQueue.get_nowait())
                except queue.Empty as e:
                    self.__timber.log('TwitchWebsocketClient', f'Encountered queue.Empty when building up dataBundles list (queue size: {self.__dataBundleQueue.qsize()}) (dataBundles size: {len(dataBundles)}): {e}', e, traceback.format_exc())

                for dataBundle in dataBundles:
                    try:
                        await dataBundleListener.onNewWebsocketDataBundle(dataBundle)
                    except Exception as e:
                        self.__timber.log('TwitchWebsocketClient', f'Encountered unknown Exception when looping through dataBundles (queue size: {self.__dataBundleQueue.qsize()}) ({dataBundle=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__queueSleepTimeSeconds)

    async def __startWebsocketConnectionFor(self, user: TwitchWebsocketUser):
        if not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        retry = True
        twitchWebsocketEndpoint = self.__twitchWebsocketEndpointHelper[user]

        while retry:
            self.__timber.log('TwitchWebsocketClient', f'Connecting to Twitch websocket ({user=}) ({twitchWebsocketEndpoint=})...')

            try:
                async with websockets.connect(twitchWebsocketEndpoint) as websocket:
                    async for message in websocket:
                        dataBundle = await self.__parseMessageToDataBundleFor(
                            message = message,
                            user = user
                        )

                        if dataBundle is None or not await self.__isValidDataBundle(dataBundle):
                            continue

                        connectionAction = await self.__twitchWebsocketConnectionActionHelper.handleConnectionRelatedActions(
                            dataBundle = dataBundle,
                            user = user
                        )

                        match connectionAction:
                            case TwitchWebsocketConnectionAction.CREATE_EVENT_SUB_SUBSCRIPTION:
                                self.__timber.log('TwitchWebsocketClient', f'Twitch websocket connection is asking for EventSub subscription(s) to be created ({user=}) ({twitchWebsocketEndpoint=}) ({connectionAction=})')
                                await self.__createEventSubSubscription(user)

                            case TwitchWebsocketConnectionAction.DISCONNECT:
                                retry = False
                                self.__timber.log('TwitchWebsocketClient', f'Twitch websocket connection was revoked when connected ({user=}) ({twitchWebsocketEndpoint=}) ({connectionAction=})')
                                await websocket.close()

                            case TwitchWebsocketConnectionAction.OK:
                                # this path is intentionally empty
                                pass

                            case TwitchWebsocketConnectionAction.RECONNECT:
                                retry = False
                                self.__timber.log('TwitchWebsocketClient', f'Twitch websocket connection is asking for a new connection to be made ({user=}) ({twitchWebsocketEndpoint=}) ({connectionAction=})')
                                self.__backgroundTaskHelper.createTask(self.__startWebsocketConnectionFor(user))

                        await self.__submitDataBundle(dataBundle)
            except Exception as e:
                instability = self.__twitchWebsocketInstabilityHelper.incrementErrorCount(user)
                self.__timber.log('TwitchWebsocketClient', f'Encountered websocket exception ({user=}) ({twitchWebsocketEndpoint=}) ({instability=}): {e}', e, traceback.format_exc())

            if retry:
                instability = self.__twitchWebsocketInstabilityHelper[user]

                if instability > self.__twitchWebsocketInstabilityThreshold:
                    oldTwitchWebsocketUrl = twitchWebsocketEndpoint
                    twitchWebsocketEndpoint = self.__twitchWebsocketEndpointHelper.resetToDefault(user)
                    self.__twitchWebsocketInstabilityHelper.resetToDefault(user)
                    self.__twitchWebsocketSessionIdHelper.resetToDefault(user)
                    self.__timber.log('TwitchWebsocketClient', f'Briefly sleeping, then will attempt to create a new Twitch websocket connection at the default URL ({user=}) ({twitchWebsocketEndpoint=}) ({instability=}) ({oldTwitchWebsocketUrl=})...')
                else:
                    self.__timber.log('TwitchWebsocketClient', f'Briefly sleeping, then will attempt to create a new Twitch websocket connection ({user=}) ({twitchWebsocketEndpoint=}) ({instability=})...')

                await asyncio.sleep(self.__websocketRetrySleepTimeSeconds)

    async def __startWebsocketConnections(self):
        users = await self.__twitchWebsocketAllowedUsersRepository.getUsers()
        self.__timber.log('TwitchWebsocketClient', f'Retrieved {len(users)} websocket user(s): ({users=})')

        for user in users:
            self.__backgroundTaskHelper.createTask(self.__startWebsocketConnectionFor(user))
            await asyncio.sleep(self.__websocketCreationDelayTimeSeconds)

        self.__timber.log('TwitchWebsocketClient', f'Finished establishing websocket connections for {len(users)} user(s)')

    async def __submitDataBundle(self, dataBundle: TwitchWebsocketDataBundle):
        if not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        try:
            self.__dataBundleQueue.put(dataBundle, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TwitchWebsocketClient', f'Encountered queue.Full when submitting a new dataBundle ({dataBundle}) into the dataBundle queue (queue size: {self.__dataBundleQueue.qsize()}): {e}', e, traceback.format_exc())
