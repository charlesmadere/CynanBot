import asyncio
import queue
import traceback
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta, timezone, tzinfo
from queue import SimpleQueue
from typing import Any, Dict, List, Optional, Set

import websockets

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.misc.incrementalJsonBuilder import IncrementalJsonBuilder
from CynanBot.misc.lruCache import LruCache
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchEventSubRequest import TwitchEventSubRequest
from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport
from CynanBot.twitch.api.websocket.twitchWebsocketTransportMethod import \
    TwitchWebsocketTransportMethod
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
        queueTimeoutSeconds: float = 3,
        websocketCreationDelayTimeSeconds: float = 0.25,
        websocketSleepTimeSeconds: float = 3,
        subscriptionTypes: Set[TwitchWebsocketSubscriptionType] = {
            TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_END,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS,
            TwitchWebsocketSubscriptionType.CHANNEL_UPDATE,
            TwitchWebsocketSubscriptionType.CHEER,
            TwitchWebsocketSubscriptionType.RAID,
            TwitchWebsocketSubscriptionType.SUBSCRIBE,
            TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT,
            TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
        },
        twitchWebsocketUrl: str = 'wss://eventsub.wss.twitch.tv/ws',
        maxMessageAge: timedelta = timedelta(minutes = 3),
        timeZone: tzinfo = timezone.utc
    ):
        assert isinstance(backgroundTaskHelper, BackgroundTaskHelper), f"malformed {backgroundTaskHelper=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchApiService, TwitchApiServiceInterface), f"malformed {twitchApiService=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(twitchWebsocketAllowedUsersRepository, TwitchWebsocketAllowedUsersRepositoryInterface), f"malformed {twitchWebsocketAllowedUsersRepository=}"
        assert isinstance(twitchWebsocketJsonMapper, TwitchWebsocketJsonMapperInterface), f"malformed {twitchWebsocketJsonMapper=}"
        if not utils.isValidNum(queueSleepTimeSeconds):
            raise ValueError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        if queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 15:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        if not utils.isValidNum(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        if queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')
        if not utils.isValidNum(websocketCreationDelayTimeSeconds):
            raise ValueError(f'websocketCreationDelayTimeSeconds argument is malformed: \"{websocketCreationDelayTimeSeconds}\"')
        if websocketCreationDelayTimeSeconds < 0.1 or websocketCreationDelayTimeSeconds > 8:
            raise ValueError(f'websocketCreationDelayTimeSeconds argument is out of bounds: {websocketCreationDelayTimeSeconds}')
        if not utils.isValidNum(websocketSleepTimeSeconds):
            raise ValueError(f'websocketSleepTimeSeconds argument is malformed: \"{websocketSleepTimeSeconds}\"')
        if websocketSleepTimeSeconds < 3 or websocketSleepTimeSeconds > 15:
            raise ValueError(f'websocketSleepTimeSeconds argument is out of bounds: {websocketSleepTimeSeconds}')
        assert isinstance(subscriptionTypes, Set), f"malformed {subscriptionTypes=}"
        if not utils.isValidUrl(twitchWebsocketUrl):
            raise ValueError(f'twitchWebsocketUrl argument is malformed: \"{twitchWebsocketUrl}\"')
        assert isinstance(maxMessageAge, timedelta), f"malformed {maxMessageAge=}"
        assert isinstance(timeZone, timezone), f"malformed {timeZone=}"

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchWebsocketAllowedUsersRepository: TwitchWebsocketAllowedUsersRepositoryInterface = twitchWebsocketAllowedUsersRepository
        self.__twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = twitchWebsocketJsonMapper
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__queueTimeoutSeconds: float = queueTimeoutSeconds
        self.__websocketCreationDelayTimeSeconds: float = websocketCreationDelayTimeSeconds
        self.__websocketSleepTimeSeconds: float = websocketSleepTimeSeconds
        self.__subscriptionTypes: Set[TwitchWebsocketSubscriptionType] = subscriptionTypes
        self.__maxMessageAge: timedelta = maxMessageAge
        self.__timeZone: tzinfo = timeZone

        self.__isStarted: bool = False
        self.__badSubscriptionTypesFor: Dict[TwitchWebsocketUser, Set[TwitchWebsocketSubscriptionType]] = defaultdict(lambda: set())
        self.__jsonBuilderFor: Dict[TwitchWebsocketUser, IncrementalJsonBuilder] = defaultdict(lambda: IncrementalJsonBuilder())
        self.__sessionIdFor: Dict[TwitchWebsocketUser, Optional[str]] = defaultdict(lambda: '')
        self.__twitchWebsocketUrlFor: Dict[TwitchWebsocketUser, str] = defaultdict(lambda: twitchWebsocketUrl)
        self.__messageIdCache: LruCache = LruCache(128)
        self.__dataBundleQueue: SimpleQueue[TwitchWebsocketDataBundle] = SimpleQueue()
        self.__dataBundleListener: Optional[TwitchWebsocketDataBundleListener] = None

    async def __createEventSubSubscription(self, sessionId: str, user: TwitchWebsocketUser):
        if not utils.isValidStr(sessionId):
            raise ValueError(f'sessionId argument is malformed: \"{sessionId}\"')
        assert isinstance(user, TwitchWebsocketUser), f"malformed {user=}"

        transport = TwitchWebsocketTransport(
            sessionId = sessionId,
            method = TwitchWebsocketTransportMethod.WEBSOCKET
        )

        await self.__twitchTokensRepository.validateAndRefreshAccessToken(user.getUserName())
        twitchAccessToken = await self.__twitchTokensRepository.requireAccessToken(user.getUserName())
        results: Dict[TwitchWebsocketSubscriptionType, Optional[Exception]] = OrderedDict()

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
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> TwitchWebsocketCondition:
        assert isinstance(user, TwitchWebsocketUser), f"malformed {user=}"
        assert isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"

        if subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_END or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK or \
                subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_UPDATE:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHEER:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.FOLLOW:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.getUserId(),
                moderatorUserId = user.getUserId()
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.RAID:
            return TwitchWebsocketCondition(
                toBroadcasterUserId = user.getUserId()
            )
        elif subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE or \
                subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT or \
                subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE:
            return TwitchWebsocketCondition(
                broadcasterUserId = user.getUserId()
            )
        else:
            raise RuntimeError(f'can\'t create a WebsocketCondition for the given unsupported WebsocketSubscriptionType: \"{subscriptionType}\"')

    async def __handleConnectionRelatedMessageFor(
        self,
        user: TwitchWebsocketUser,
        dataBundle: TwitchWebsocketDataBundle
    ):
        assert isinstance(user, TwitchWebsocketUser), f"malformed {user=}"
        assert isinstance(dataBundle, TwitchWebsocketDataBundle), f"malformed {dataBundle=}"

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
        assert oldSessionId is None or isinstance(oldSessionId, str), f"malformed {oldSessionId=}"
        assert isinstance(user, TwitchWebsocketUser), f"malformed {user=}"

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
        if not utils.isValidUrl(oldTwitchWebsocketUrl):
            raise ValueError(f'oldTwitchWebsocketUrl argument is malformed: \"{oldTwitchWebsocketUrl}\"')
        assert isinstance(user, TwitchWebsocketUser), f"malformed {user=}"

        self.__twitchWebsocketUrlFor[user] = newTwitchWebsocketUrl
        self.__timber.log('TwitchWebsocketClient', f'Twitch websocket URL for \"{user}\" has been changed to \"{newTwitchWebsocketUrl}\" from \"{oldTwitchWebsocketUrl}\"')

    async def __isValidMessage(self, dataBundle: TwitchWebsocketDataBundle) -> bool:
        assert isinstance(dataBundle, TwitchWebsocketDataBundle), f"malformed {dataBundle=}"

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
    ) -> Optional[List[TwitchWebsocketDataBundle]]:
        assert isinstance(user, TwitchWebsocketUser), f"malformed {user=}"

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

        dataBundles: List[TwitchWebsocketDataBundle] = list()

        for index, dictionary in enumerate(dictionaries):
            dataBundle: Optional[TwitchWebsocketDataBundle] = None
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
        assert listener is None or isinstance(listener, TwitchWebsocketDataBundleListener), f"malformed {listener=}"

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
                dataBundles: List[TwitchWebsocketDataBundle] = list()

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
        assert isinstance(user, TwitchWebsocketUser), f"malformed {user=}"

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
        assert isinstance(dataBundle, TwitchWebsocketDataBundle), f"malformed {dataBundle=}"

        try:
            self.__dataBundleQueue.put(dataBundle, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TwitchWebsocketClient', f'Encountered queue.Full when submitting a new dataBundle ({dataBundle}) into the dataBundle queue (queue size: {self.__dataBundleQueue.qsize()}): {e}', e, traceback.format_exc())
