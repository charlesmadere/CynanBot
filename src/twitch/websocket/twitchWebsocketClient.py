import asyncio
import queue
import traceback
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from queue import SimpleQueue
from typing import Any

import websockets
from location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from misc.incrementalJsonBuilder import IncrementalJsonBuilder
from misc.lruCache import LruCache
from timber.timberInterface import TimberInterface
from twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from twitch.api.twitchEventSubRequest import TwitchEventSubRequest
from twitch.api.twitchEventSubResponse import TwitchEventSubResponse
from twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport
from twitch.api.websocket.twitchWebsocketTransportMethod import \
    TwitchWebsocketTransportMethod
from twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from twitch.websocket.twitchWebsocketAllowedUsersRepositoryInterface import \
    TwitchWebsocketAllowedUsersRepositoryInterface
from twitch.websocket.twitchWebsocketClientInterface import \
    TwitchWebsocketClientInterface
from twitch.websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener
from twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface
from twitch.websocket.twitchWebsocketUser import TwitchWebsocketUser

from ..misc import utils as utils


class TwitchWebsocketClient(TwitchWebsocketClientInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchWebsocketAllowedUsersRepository: TwitchWebsocketAllowedUsersRepositoryInterface,
        twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface,
        queueSleepTimeSeconds: float = 1,
        queueTimeoutSeconds: float = 3,
        websocketCreationDelayTimeSeconds: float = 0.25,
        websocketSleepTimeSeconds: float = 3,
        subscriptionTypes: set[TwitchWebsocketSubscriptionType] = {
            TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_END,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS,
            TwitchWebsocketSubscriptionType.CHEER,
            TwitchWebsocketSubscriptionType.FOLLOW,
            TwitchWebsocketSubscriptionType.RAID,
            TwitchWebsocketSubscriptionType.SUBSCRIBE,
            TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT,
            TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
        },
        twitchWebsocketUrl: str = 'wss://eventsub.wss.twitch.tv/ws',
        maxMessageAge: timedelta = timedelta(minutes = 3)
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
        elif not isinstance(twitchWebsocketJsonMapper, TwitchWebsocketJsonMapperInterface):
            raise TypeError(f'twitchWebsocketJsonMapper argument is malformed: \"{twitchWebsocketJsonMapper}\"')
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
        elif not utils.isValidNum(websocketSleepTimeSeconds):
            raise TypeError(f'websocketSleepTimeSeconds argument is malformed: \"{websocketSleepTimeSeconds}\"')
        elif websocketSleepTimeSeconds < 3 or websocketSleepTimeSeconds > 15:
            raise ValueError(f'websocketSleepTimeSeconds argument is out of bounds: {websocketSleepTimeSeconds}')
        elif not isinstance(subscriptionTypes, set):
            raise TypeError(f'subscriptionTypes argument is malformed: \"{subscriptionTypes}\"')
        elif not utils.isValidUrl(twitchWebsocketUrl):
            raise TypeError(f'twitchWebsocketUrl argument is malformed: \"{twitchWebsocketUrl}\"')
        elif not isinstance(maxMessageAge, timedelta):
            raise TypeError(f'maxMessageAge argument is malformed: \"{maxMessageAge}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchWebsocketAllowedUsersRepository: TwitchWebsocketAllowedUsersRepositoryInterface = twitchWebsocketAllowedUsersRepository
        self.__twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = twitchWebsocketJsonMapper
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__queueTimeoutSeconds: float = queueTimeoutSeconds
        self.__websocketCreationDelayTimeSeconds: float = websocketCreationDelayTimeSeconds
        self.__websocketSleepTimeSeconds: float = websocketSleepTimeSeconds
        self.__subscriptionTypes: set[TwitchWebsocketSubscriptionType] = subscriptionTypes
        self.__maxMessageAge: timedelta = maxMessageAge

        self.__isStarted: bool = False
        self.__badSubscriptionTypesFor: dict[TwitchWebsocketUser, set[TwitchWebsocketSubscriptionType]] = defaultdict(lambda: set())
        self.__jsonBuilderFor: dict[TwitchWebsocketUser, IncrementalJsonBuilder] = defaultdict(lambda: IncrementalJsonBuilder())
        self.__sessionIdFor: dict[TwitchWebsocketUser, str | None] = defaultdict(lambda: '')
        self.__twitchWebsocketUrlFor: dict[TwitchWebsocketUser, str] = defaultdict(lambda: twitchWebsocketUrl)
        self.__messageIdCache: LruCache = LruCache(128)
        self.__dataBundleQueue: SimpleQueue[TwitchWebsocketDataBundle] = SimpleQueue()
        self.__dataBundleListener: TwitchWebsocketDataBundleListener | None = None

    async def __createEventSubSubscription(self, sessionId: str, user: TwitchWebsocketUser):
        if not utils.isValidStr(sessionId):
            raise TypeError(f'sessionId argument is malformed: \"{sessionId}\"')
        elif not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        transport = TwitchWebsocketTransport(
            sessionId = sessionId,
            method = TwitchWebsocketTransportMethod.WEBSOCKET
        )

        twitchAccessToken = await self.__twitchTokensRepository.requireAccessTokenById(user.userId)
        results: dict[TwitchWebsocketSubscriptionType, Exception | None] = OrderedDict()

        for subscriptionType in self.__subscriptionTypes:
            if subscriptionType in self.__badSubscriptionTypesFor[user]:
                self.__timber.log('TwitchWebsocketClient', f'Skipping {subscriptionType} for {user}')
                continue

            condition = await self.__createWebsocketCondition(
                user = user,
                subscriptionType = subscriptionType
            )

            eventSubRequest = TwitchEventSubRequest(
                condition = condition,
                subscriptionType = subscriptionType,
                transport = transport
            )

            response: TwitchEventSubResponse | None = None
            exception: Exception | None = None

            try:
                response = await self.__twitchApiService.createEventSubSubscription(
                    twitchAccessToken = twitchAccessToken,
                    eventSubRequest = eventSubRequest
                )
            except Exception as e:
                exception = e

            results[subscriptionType] = exception

            if response is None or exception is not None:
                self.__badSubscriptionTypesFor[user].add(subscriptionType)

        self.__timber.log('TwitchWebsocketClient', f'Finished creating EventSub subscription(s) for {user}: {results}')

    async def __createWebsocketCondition(
        self,
        user: TwitchWebsocketUser,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> TwitchWebsocketCondition:
        if not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        if subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_END or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_UPDATE:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHEER:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.FOLLOW:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId,
                moderatorUserId = user.userId
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.RAID:
            return TwitchWebsocketCondition(
                toBroadcasterUserId = user.userId
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE or \
                subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT or \
                subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.userId
            )
        else:
            raise RuntimeError(f'can\'t create a WebsocketCondition for the given unsupported WebsocketSubscriptionType: \"{subscriptionType}\"')

    async def __handleConnectionRelatedMessageFor(
        self,
        user: TwitchWebsocketUser,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        payload = dataBundle.payload

        if payload is None:
            return

        session = payload.session

        if session is None:
            return

        oldTwitchWebsocketUrl = self.__twitchWebsocketUrlFor[user]
        newTwitchWebsocketUrl = session.reconnectUrl

        if utils.isValidUrl(newTwitchWebsocketUrl) and oldTwitchWebsocketUrl != newTwitchWebsocketUrl:
            await self.__handleNewTwitchWebsocketUrlFor(
                newTwitchWebsocketUrl = newTwitchWebsocketUrl,
                oldTwitchWebsocketUrl = oldTwitchWebsocketUrl,
                user = user
            )

        oldSessionId = self.__sessionIdFor[user]
        newSessionId = session.sessionId

        if oldSessionId != newSessionId:
            await self.__handleNewSessionIdFor(
                newSessionId = newSessionId,
                oldSessionId = oldSessionId,
                user = user
            )

    async def __handleNewSessionIdFor(
        self,
        newSessionId: str,
        oldSessionId: str | None,
        user: TwitchWebsocketUser
    ):
        if not utils.isValidStr(newSessionId):
            raise TypeError(f'newSessionId argument is malformed: \"{newSessionId}\"')
        elif oldSessionId is not None and not isinstance(oldSessionId, str):
            raise TypeError(f'oldSessionId argument is malformed: \"{oldSessionId}\"')
        elif not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        self.__sessionIdFor[user] = newSessionId
        self.__timber.log('TwitchWebsocketClient', f'Session ID for \"{user}\" has been changed to \"{newSessionId}\" from \"{oldSessionId}\". Creating EventSub subscription(s)...')

        await self.__createEventSubSubscription(
            sessionId = newSessionId,
            user = user
        )

    async def __handleNewTwitchWebsocketUrlFor(
        self,
        newTwitchWebsocketUrl: str,
        oldTwitchWebsocketUrl: str,
        user: TwitchWebsocketUser
    ):
        if not utils.isValidUrl(newTwitchWebsocketUrl):
            raise TypeError(f'newTwitchWebsocketUrl argument is malformed: \"{newTwitchWebsocketUrl}\"')
        elif not utils.isValidUrl(oldTwitchWebsocketUrl):
            raise TypeError(f'oldTwitchWebsocketUrl argument is malformed: \"{oldTwitchWebsocketUrl}\"')
        elif not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        self.__twitchWebsocketUrlFor[user] = newTwitchWebsocketUrl
        self.__timber.log('TwitchWebsocketClient', f'Twitch websocket URL for \"{user}\" has been changed to \"{newTwitchWebsocketUrl}\" from \"{oldTwitchWebsocketUrl}\"')

    async def __isValidMessage(self, dataBundle: TwitchWebsocketDataBundle) -> bool:
        if not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        # ensure that this isn't a message we've seen before
        if self.__messageIdCache.contains(dataBundle.metadata.messageId):
            self.__timber.log('TwitchWebsocketClient', f'Encountered a message ID that has already been seen: \"{dataBundle.metadata.messageId}\"')
            return False

        self.__messageIdCache.put(dataBundle.metadata.messageId)

        # ensure that this message isn't gratuitously old
        messageTimestamp = dataBundle.metadata.messageTimestamp
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if now - messageTimestamp >= self.__maxMessageAge:
            self.__timber.log('TwitchWebsocketClient', f'Encountered a message that is too old: \"{dataBundle.metadata.messageId}\"')
            return False

        return True

    async def __parseMessageToDataBundlesFor(
        self,
        message: Any | None,
        user: TwitchWebsocketUser
    ) -> list[TwitchWebsocketDataBundle] | None:
        if not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if message is None:
            self.__timber.log('TwitchWebsocketClient', f'Received message object that is None: \"{message}\"')
            return None
        elif not isinstance(message, str):
            self.__timber.log('TwitchWebsocketClient', f'Received message object that is of an unexpected type: \"{message}\"')
            return None

        jsonBuilder = self.__jsonBuilderFor[user]
        dictionaries = await jsonBuilder.buildDictionariesOrAppendInternalJsonCache(message)

        if not utils.hasItems(dictionaries):
            return None

        dataBundles: list[TwitchWebsocketDataBundle] = list()

        for index, dictionary in enumerate(dictionaries):
            dataBundle: TwitchWebsocketDataBundle | None = None
            exception: Exception | None = None

            try:
                dataBundle = await self.__twitchWebsocketJsonMapper.parseWebsocketDataBundle(dictionary)
            except Exception as e:
                exception = e

            if exception is not None:
                self.__timber.log('TwitchWebsocketClient', f'Encountered an exception when attempting to convert dictionary ({dictionary}) at index {index} into WebsocketDataBundle: {exception}', exception, traceback.format_exc())
                continue
            elif dataBundle is None:
                self.__timber.log('TwitchWebsocketClient', f'Received `None` when attempting to convert dictionary at index {index} into WebsocketDataBundle: \"{dictionary}\"')
                continue

            dataBundles.append(dataBundle)

        if utils.hasItems(dataBundles):
            return dataBundles
        else:
            return None

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
                    if not await self.__isValidMessage(dataBundle):
                        continue

                    try:
                        await dataBundleListener.onNewWebsocketDataBundle(dataBundle)
                    except Exception as e:
                        self.__timber.log('RecurringActionsMachine', f'Encountered unknown Exception when looping through dataBundles (queue size: {self.__dataBundleQueue.qsize()}) ({dataBundle=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__queueSleepTimeSeconds)

    async def __startWebsocketConnectionFor(self, user: TwitchWebsocketUser):
        if not isinstance(user, TwitchWebsocketUser):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        while True:
            twitchWebsocketUrl = self.__twitchWebsocketUrlFor[user]
            self.__timber.log('TwitchWebsocketClient', f'Connecting to websocket \"{twitchWebsocketUrl}\" for \"{user}\"...')

            try:
                async with websockets.connect(twitchWebsocketUrl) as websocket:
                    async for message in websocket:
                        dataBundles = await self.__parseMessageToDataBundlesFor(message, user)

                        if dataBundles is None or len(dataBundles) == 0:
                            continue

                        for dataBundle in dataBundles:
                            await self.__handleConnectionRelatedMessageFor(user, dataBundle)
                            await self.__submitDataBundle(dataBundle)
            except Exception as e:
                self.__timber.log('TwitchWebsocketClient', f'Encountered websocket exception for \"{user}\" when connected to \"{twitchWebsocketUrl}\": {e}', e, traceback.format_exc())
                self.__sessionIdFor[user] = ''

            await asyncio.sleep(self.__websocketSleepTimeSeconds)

    async def __startWebsocketConnections(self):
        users = await self.__twitchWebsocketAllowedUsersRepository.getUsers()
        self.__timber.log('TwitchWebsocketClient', f'Retrieved {len(users)} websocket user(s)')

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
