import asyncio
import queue
import traceback
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta, timezone
from queue import SimpleQueue
from typing import Any, Dict, List, Optional, Set

import websockets

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.incrementalJsonBuilder import IncrementalJsonBuilder
from CynanBot.misc.lruCache import LruCache
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.twitchApiServiceInterface import TwitchApiServiceInterface
from CynanBot.twitch.twitchEventSubRequest import TwitchEventSubRequest
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.twitch.websocket.twitchWebsocketAllowedUsersRepositoryInterface import \
    TwitchWebsocketAllowedUsersRepositoryInterface
from CynanBot.twitch.websocket.twitchWebsocketClientInterface import \
    TwitchWebsocketClientInterface
from CynanBot.twitch.websocket.twitchWebsocketDataBundleListener import \
    TwitchWebsocketDataBundleListener
from CynanBot.twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface
from CynanBot.twitch.websocket.twitchWebsocketUser import TwitchWebsocketUser
from CynanBot.twitch.websocket.websocketCondition import WebsocketCondition
from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBot.twitch.websocket.websocketTransport import WebsocketTransport
from CynanBot.twitch.websocket.websocketTransportMethod import \
    WebsocketTransportMethod


class TwitchWebsocketClient(TwitchWebsocketClientInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchWebsocketAllowedUsersRepository: TwitchWebsocketAllowedUsersRepositoryInterface,
        twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface,
        queueSleepTimeSeconds: float = 1,
        websocketCreationDelayTimeSeconds: float = 0.25,
        websocketSleepTimeSeconds: float = 3,
        queueTimeoutSeconds: int = 3,
        subscriptionTypes: Set[WebsocketSubscriptionType] = {
            WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION,
            WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN,
            WebsocketSubscriptionType.CHANNEL_PREDICTION_END,
            WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK,
            WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS,
            WebsocketSubscriptionType.CHANNEL_UPDATE,
            WebsocketSubscriptionType.CHEER,
            WebsocketSubscriptionType.RAID,
            WebsocketSubscriptionType.SUBSCRIBE,
            WebsocketSubscriptionType.SUBSCRIPTION_GIFT,
            WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
        },
        twitchWebsocketUrl: str = 'wss://eventsub.wss.twitch.tv/ws',
        maxMessageAge: timedelta = timedelta(minutes = 10),
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise ValueError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise ValueError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchWebsocketAllowedUsersRepository, TwitchWebsocketAllowedUsersRepositoryInterface):
            raise ValueError(f'twitchWebsocketAllowedUsersRepository argument is malformed: \"{twitchWebsocketAllowedUsersRepository}\"')
        elif not isinstance(twitchWebsocketJsonMapper, TwitchWebsocketJsonMapperInterface):
            raise ValueError(f'twitchWebsocketJsonMapper argument is malformed: \"{twitchWebsocketJsonMapper}\"')
        elif not utils.isValidNum(queueSleepTimeSeconds):
            raise ValueError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 15:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        elif not utils.isValidNum(websocketCreationDelayTimeSeconds):
            raise ValueError(f'websocketCreationDelayTimeSeconds argument is malformed: \"{websocketCreationDelayTimeSeconds}\"')
        elif websocketCreationDelayTimeSeconds < 0.1 or websocketCreationDelayTimeSeconds > 8:
            raise ValueError(f'websocketCreationDelayTimeSeconds argument is out of bounds: {websocketCreationDelayTimeSeconds}')
        elif not utils.isValidNum(websocketSleepTimeSeconds):
            raise ValueError(f'websocketSleepTimeSeconds argument is malformed: \"{websocketSleepTimeSeconds}\"')
        elif websocketSleepTimeSeconds < 3 or websocketSleepTimeSeconds > 15:
            raise ValueError(f'websocketSleepTimeSeconds argument is out of bounds: {websocketSleepTimeSeconds}')
        elif not utils.isValidNum(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')
        elif not isinstance(subscriptionTypes, Set):
            raise ValueError(f'subscriptionTypes argument is malformed: \"{subscriptionTypes}\"')
        elif not utils.isValidUrl(twitchWebsocketUrl):
            raise ValueError(f'twitchWebsocketUrl argument is malformed: \"{twitchWebsocketUrl}\"')
        elif not isinstance(maxMessageAge, timedelta):
            raise ValueError(f'maxMessageAge argument is malformed: \"{maxMessageAge}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchWebsocketAllowedUsersRepository: TwitchWebsocketAllowedUsersRepositoryInterface = twitchWebsocketAllowedUsersRepository
        self.__twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = twitchWebsocketJsonMapper
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__websocketCreationDelayTimeSeconds: float = websocketCreationDelayTimeSeconds
        self.__websocketSleepTimeSeconds: float = websocketSleepTimeSeconds
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds
        self.__subscriptionTypes: Set[WebsocketSubscriptionType] = subscriptionTypes
        self.__maxMessageAge: timedelta = maxMessageAge
        self.__timeZone: timezone = timeZone

        self.__isStarted: bool = False
        self.__badSubscriptionTypesFor: Dict[TwitchWebsocketUser, Set[WebsocketSubscriptionType]] = defaultdict(lambda: set())
        self.__jsonBuilderFor: Dict[TwitchWebsocketUser, IncrementalJsonBuilder] = defaultdict(lambda: IncrementalJsonBuilder())
        self.__sessionIdFor: Dict[TwitchWebsocketUser, Optional[str]] = defaultdict(lambda: '')
        self.__twitchWebsocketUrlFor: Dict[TwitchWebsocketUser, str] = defaultdict(lambda: twitchWebsocketUrl)
        self.__messageIdCache: LruCache = LruCache(128)
        self.__dataBundleQueue: SimpleQueue[WebsocketDataBundle] = SimpleQueue()
        self.__dataBundleListener: Optional[TwitchWebsocketDataBundleListener] = None

    async def __createEventSubSubscription(self, sessionId: str, user: TwitchWebsocketUser):
        if not utils.isValidStr(sessionId):
            raise ValueError(f'sessionId argument is malformed: \"{sessionId}\"')
        elif not isinstance(user, TwitchWebsocketUser):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        transport = WebsocketTransport(
            sessionId = sessionId,
            method = WebsocketTransportMethod.WEBSOCKET
        )

        await self.__twitchTokensRepository.validateAndRefreshAccessToken(user.getUserName())
        twitchAccessToken = await self.__twitchTokensRepository.requireAccessToken(user.getUserName())
        results: Dict[WebsocketSubscriptionType, Optional[Exception]] = OrderedDict()

        for subscriptionType in self.__subscriptionTypes:
            if subscriptionType in self.__badSubscriptionTypesFor[user]:
                self.__timber.log('TwitchWebsocketClient', f'Skipping {subscriptionType} for \"{user}\"')
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

            exception: Optional[Exception] = None

            try:
                await self.__twitchApiService.createEventSubSubscription(
                    twitchAccessToken = twitchAccessToken,
                    eventSubRequest = eventSubRequest
                )
            except Exception as e:
                exception = e

            results[subscriptionType] = exception

            if exception is not None:
                self.__badSubscriptionTypesFor[user].add(subscriptionType)

        self.__timber.log('TwitchWebsocketClient', f'Finished creating EventSub subscription(s) for {user}: {results}')

    async def __createWebsocketCondition(
        self,
        user: TwitchWebsocketUser,
        subscriptionType: WebsocketSubscriptionType
    ) -> WebsocketCondition:
        if not isinstance(user, TwitchWebsocketUser):
            raise ValueError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(subscriptionType, WebsocketSubscriptionType):
            raise ValueError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        if subscriptionType is WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            return WebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        elif subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN or \
                subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_END or \
                subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK or \
                subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return WebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        elif subscriptionType is WebsocketSubscriptionType.CHANNEL_UPDATE:
            return WebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        elif subscriptionType is WebsocketSubscriptionType.CHEER:
            return WebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        elif subscriptionType is WebsocketSubscriptionType.FOLLOW:
            return WebsocketCondition(
                broadcasterUserId = user.getUserId(),
                moderatorUserId = user.getUserId()
            )
        elif subscriptionType is WebsocketSubscriptionType.RAID:
            return WebsocketCondition(
                toBroadcasterUserId = user.getUserId()
            )
        elif subscriptionType is WebsocketSubscriptionType.SUBSCRIBE or \
                subscriptionType is WebsocketSubscriptionType.SUBSCRIPTION_GIFT or \
                subscriptionType is WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE:
            return WebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        else:
            raise RuntimeError(f'can\'t create a WebsocketCondition for the given unsupported WebsocketSubscriptionType: \"{subscriptionType}\"')

    async def __handleConnectionRelatedMessageFor(
        self,
        user: TwitchWebsocketUser,
        dataBundle: WebsocketDataBundle
    ):
        if not isinstance(user, TwitchWebsocketUser):
            raise ValueError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        payload = dataBundle.getPayload()

        if payload is None:
            return

        session = payload.getSession()

        if session is None:
            return

        oldTwitchWebsocketUrl = self.__twitchWebsocketUrlFor[user]
        newTwitchWebsocketUrl = session.getReconnectUrl()

        if utils.isValidUrl(newTwitchWebsocketUrl) and oldTwitchWebsocketUrl != newTwitchWebsocketUrl:
            await self.__handleNewTwitchWebsocketUrlFor(
                newTwitchWebsocketUrl = newTwitchWebsocketUrl,
                oldTwitchWebsocketUrl = oldTwitchWebsocketUrl,
                user = user
            )

        oldSessionId = self.__sessionIdFor[user]
        newSessionId = session.getSessionId()

        if oldSessionId != newSessionId:
            await self.__handleNewSessionIdFor(
                newSessionId = newSessionId,
                oldSessionId = oldSessionId,
                user = user
            )

    async def __handleNewSessionIdFor(
        self,
        newSessionId: str,
        oldSessionId: Optional[str],
        user: TwitchWebsocketUser
    ):
        if not utils.isValidStr(newSessionId):
            raise ValueError(f'newSessionId argument is malformed: \"{newSessionId}\"')
        elif oldSessionId is not None and not isinstance(oldSessionId, str):
            raise ValueError(f'oldSessionId argument is malformed: \"{oldSessionId}\"')
        elif not isinstance(user, TwitchWebsocketUser):
            raise ValueError(f'user argument is malformed: \"{user}\"')

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
            raise ValueError(f'newTwitchWebsocketUrl argument is malformed: \"{newTwitchWebsocketUrl}\"')
        elif not utils.isValidUrl(oldTwitchWebsocketUrl):
            raise ValueError(f'oldTwitchWebsocketUrl argument is malformed: \"{oldTwitchWebsocketUrl}\"')
        elif not isinstance(user, TwitchWebsocketUser):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        self.__twitchWebsocketUrlFor[user] = newTwitchWebsocketUrl
        self.__timber.log('TwitchWebsocketClient', f'Twitch websocket URL for \"{user}\" has been changed to \"{newTwitchWebsocketUrl}\" from \"{oldTwitchWebsocketUrl}\"')

    async def __isValidMessage(self, dataBundle: WebsocketDataBundle) -> bool:
        if not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        # ensure that this isn't a message we've seen before
        if self.__messageIdCache.contains(dataBundle.getMetadata().getMessageId()):
            self.__timber.log('TwitchWebsocketClient', f'Encountered a message ID that has already been seen: \"{dataBundle.getMetadata().getMessageId()}\"')
            return False

        self.__messageIdCache.put(dataBundle.getMetadata().getMessageId())

        # ensure that this message isn't gratuitously old
        messageTimestamp = dataBundle.getMetadata().getMessageTimestamp().getDateTime()
        now = datetime.now(self.__timeZone)

        if now - messageTimestamp >= self.__maxMessageAge:
            self.__timber.log('TwitchWebsocketClient', f'Encountered a message that is too old: \"{dataBundle.getMetadata().getMessageId()}\"')
            return False

        return True

    async def __parseMessageToDataBundlesFor(
        self,
        message: Optional[Any],
        user: TwitchWebsocketUser
    ) -> Optional[List[WebsocketDataBundle]]:
        if not isinstance(user, TwitchWebsocketUser):
            raise ValueError(f'user argument is malformed: \"{user}\"')

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

        dataBundles: List[WebsocketDataBundle] = list()

        for index, dictionary in enumerate(dictionaries):
            dataBundle: Optional[WebsocketDataBundle] = None
            exception: Optional[Exception] = None

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

    def setDataBundleListener(self, listener: Optional[TwitchWebsocketDataBundleListener]):
        if listener is not None and not isinstance(listener, TwitchWebsocketDataBundleListener):
            raise ValueError(f'listener argument is malformed: \"{listener}\"')

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
                dataBundles: List[WebsocketDataBundle] = list()

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
            raise ValueError(f'user argument is malformed: \"{user}\"')

        while True:
            twitchWebsocketUrl = self.__twitchWebsocketUrlFor[user]
            self.__timber.log('TwitchWebsocketClient', f'Connecting to websocket \"{twitchWebsocketUrl}\" for \"{user}\"...')

            try:
                async with websockets.connect(twitchWebsocketUrl) as websocket:
                    async for message in websocket:
                        dataBundles = await self.__parseMessageToDataBundlesFor(message, user)

                        if not utils.hasItems(dataBundles):
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

    async def __submitDataBundle(self, dataBundle: WebsocketDataBundle):
        if not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        try:
            self.__dataBundleQueue.put(dataBundle, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TwitchWebsocketClient', f'Encountered queue.Full when submitting a new dataBundle ({dataBundle}) into the dataBundle queue (queue size: {self.__dataBundleQueue.qsize()}): {e}', e, traceback.format_exc())
