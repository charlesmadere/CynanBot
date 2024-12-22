import asyncio
import json
import queue
import traceback
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from enum import Enum, auto
from queue import SimpleQueue
from typing import Any

import websockets

from ..api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..api.twitchEventSubRequest import TwitchEventSubRequest
from ..api.twitchEventSubResponse import TwitchEventSubResponse
from ..api.websocket.twitchWebsocketCondition import TwitchWebsocketCondition
from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.websocket.twitchWebsocketMessageType import TwitchWebsocketMessageType
from ..api.websocket.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..api.websocket.twitchWebsocketTransport import TwitchWebsocketTransport
from ..api.websocket.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod
from ..twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..websocket.twitchWebsocketAllowedUsersRepositoryInterface import TwitchWebsocketAllowedUsersRepositoryInterface
from ..websocket.twitchWebsocketClientInterface import TwitchWebsocketClientInterface
from ..websocket.twitchWebsocketDataBundleListener import TwitchWebsocketDataBundleListener
from ..websocket.twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from ..websocket.twitchWebsocketUser import TwitchWebsocketUser
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...misc.lruCache import LruCache
from ...timber.timberInterface import TimberInterface


class TwitchWebsocketClient(TwitchWebsocketClientInterface):

    class ConnectionAction(Enum):
        CREATE_EVENT_SUB_SUBSCRIPTION = auto()
        DISCONNECT = auto()
        OK = auto()
        RECONNECT = auto()

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchWebsocketAllowedUsersRepository: TwitchWebsocketAllowedUsersRepositoryInterface,
        twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface,
        isFullJsonLoggingEnabled: bool = False,
        queueSleepTimeSeconds: float = 1,
        queueTimeoutSeconds: float = 3,
        websocketCreationDelayTimeSeconds: float = 0.5,
        subscriptionTypes: frozenset[TwitchWebsocketSubscriptionType] = frozenset({
            TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_END,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS,
            TwitchWebsocketSubscriptionType.CHEER,
            TwitchWebsocketSubscriptionType.RAID,
            TwitchWebsocketSubscriptionType.SUBSCRIBE,
            TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT,
            TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
        }),
        twitchWebsocketUrl: str = 'wss://eventsub.wss.twitch.tv/ws',
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
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchWebsocketAllowedUsersRepository, TwitchWebsocketAllowedUsersRepositoryInterface):
            raise TypeError(f'twitchWebsocketAllowedUsersRepository argument is malformed: \"{twitchWebsocketAllowedUsersRepository}\"')
        elif not isinstance(twitchWebsocketJsonMapper, TwitchWebsocketJsonMapperInterface):
            raise TypeError(f'twitchWebsocketJsonMapper argument is malformed: \"{twitchWebsocketJsonMapper}\"')
        elif not utils.isValidBool(isFullJsonLoggingEnabled):
            raise TypeError(f'isFullJsonLoggingEnabled argument is malformed: \"{isFullJsonLoggingEnabled}\"')
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
        elif not isinstance(subscriptionTypes, frozenset):
            raise TypeError(f'subscriptionTypes argument is malformed: \"{subscriptionTypes}\"')
        elif not utils.isValidUrl(twitchWebsocketUrl):
            raise TypeError(f'twitchWebsocketUrl argument is malformed: \"{twitchWebsocketUrl}\"')
        elif not isinstance(maxMessageAge, timedelta):
            raise TypeError(f'maxMessageAge argument is malformed: \"{maxMessageAge}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchWebsocketAllowedUsersRepository: TwitchWebsocketAllowedUsersRepositoryInterface = twitchWebsocketAllowedUsersRepository
        self.__twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = twitchWebsocketJsonMapper
        self.__isFullJsonLoggingEnabled: bool = isFullJsonLoggingEnabled
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__queueTimeoutSeconds: float = queueTimeoutSeconds
        self.__subscriptionTypes: frozenset[TwitchWebsocketSubscriptionType] = subscriptionTypes
        self.__maxMessageAge: timedelta = maxMessageAge

        self.__isStarted: bool = False
        self.__badSubscriptionTypesFor: dict[TwitchWebsocketUser, set[TwitchWebsocketSubscriptionType]] = defaultdict(lambda: set())
        # self.__sessionIdFor: dict[TwitchWebsocketUser, str | None] = defaultdict(lambda: '')
        # self.__twitchWebsocketUrlFor: dict[TwitchWebsocketUser, str] = defaultdict(lambda: twitchWebsocketUrl)
        self.__messageIdCache: LruCache = LruCache(128)
        self.__dataBundleQueue: SimpleQueue[TwitchWebsocketDataBundle] = SimpleQueue()
        self.__twitchSessionId: str | None = None
        self.__twitchWebsocketUrl: str = twitchWebsocketUrl
        self.__dataBundleListener: TwitchWebsocketDataBundleListener | None = None

    async def __createEventSubSubscription(self):
        sessionId = self.__twitchSessionId

        if not utils.isValidStr(sessionId):
            self.__timber.log('TwitchWebsocketClient', f'Skipping creation of EventSub subscription(s) ({sessionId=})')
            return

        transport = TwitchWebsocketTransport(
            sessionId = sessionId,
            method = TwitchWebsocketTransportMethod.WEBSOCKET
        )

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchAccessToken = await self.__twitchTokensRepository.requireAccessToken(twitchHandle)
        users = await self.__twitchWebsocketAllowedUsersRepository.getUsers()
        results: dict[TwitchWebsocketSubscriptionType, Exception | None] = OrderedDict()

        for subscriptionType in self.__subscriptionTypes:
            for user in users:
                if subscriptionType in self.__badSubscriptionTypesFor[user]:
                    self.__timber.log('TwitchWebsocketClient', f'Skipping creation of EventSub subscription for {user} ({subscriptionType=}) ({sessionId=})')
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

        self.__timber.log('TwitchWebsocketClient', f'Finished creating EventSub subscription(s) ({sessionId=}) ({results=})')

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
        dataBundle: TwitchWebsocketDataBundle
    ) -> ConnectionAction:
        if not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        if dataBundle.payload is not None and dataBundle.payload.session is not None:
            session = dataBundle.payload.session

            oldTwitchWebsocketUrl = self.__twitchWebsocketUrl
            newTwitchWebsocketUrl = session.reconnectUrl
            oldSessionId = self.__twitchSessionId
            newSessionId = session.sessionId

            if utils.isValidUrl(newTwitchWebsocketUrl) and oldTwitchWebsocketUrl != newTwitchWebsocketUrl:
                self.__twitchWebsocketUrl = newTwitchWebsocketUrl
                self.__timber.log('TwitchWebsocketClient', f'Twitch websocket URL has been changed ({newTwitchWebsocketUrl=}) ({oldTwitchWebsocketUrl=}) ({dataBundle=})')

            if utils.isValidStr(newSessionId) and oldSessionId != newSessionId:
                self.__twitchSessionId = newSessionId
                self.__timber.log('TwitchWebsocketClient', f'Twitch session ID has been changed ({newSessionId=}) ({oldSessionId=}) ({dataBundle=})')

        match dataBundle.metadata.messageType:
            case TwitchWebsocketMessageType.KEEP_ALIVE:
                return TwitchWebsocketClient.ConnectionAction.OK

            case TwitchWebsocketMessageType.NOTIFICATION:
                return TwitchWebsocketClient.ConnectionAction.OK

            case TwitchWebsocketMessageType.RECONNECT:
                return TwitchWebsocketClient.ConnectionAction.RECONNECT

            case TwitchWebsocketMessageType.REVOCATION:
                return TwitchWebsocketClient.ConnectionAction.DISCONNECT

            case TwitchWebsocketMessageType.WELCOME:
                return TwitchWebsocketClient.ConnectionAction.CREATE_EVENT_SUB_SUBSCRIPTION

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

    async def __parseMessageToDataBundleFor(
        self,
        message: str | Any | None
    ) -> TwitchWebsocketDataBundle | None:
        if message is None:
            self.__timber.log('TwitchWebsocketClient', f'Received a None message instance: ({message=})')
            return None
        elif not isinstance(message, str):
            self.__timber.log('TwitchWebsocketClient', f'Received a message instance that is of an unexpected type: ({message=})')
            return None
        elif not utils.isValidStr(message):
            self.__timber.log('TwitchWebsocketClient', f'Received an empty/blank message String: ({message=})')
            return None

        dictionary: dict[str, Any] | Any | None = None

        try:
            dictionary = json.loads(message)
        except Exception as e:
            self.__timber.log('TwitchWebsocketClient', f'Encountered an exception when attempting to parse message into JSON dictionary ({dictionary=}) ({message=}): {e}', e, traceback.format_exc())
            return None

        if not isinstance(dictionary, dict) or len(dictionary) == 0:
            self.__timber.log('TwitchWebsocketClient', f'Message was parsed into an unexpected or malformed type ({dictionary=}) ({message=})')
            return None

        dataBundle: TwitchWebsocketDataBundle | None = None
        exception: Exception | None = None

        try:
            dataBundle = await self.__twitchWebsocketJsonMapper.parseWebsocketDataBundle(dictionary)
        except Exception as e:
            exception = e

        if self.__isFullJsonLoggingEnabled:
            self.__timber.log('TwitchWebsocketClient', f'Full message output: ({message=})')
            self.__timber.log('TwitchWebsocketClient', f'Full JSON output: ({dictionary=})')
            self.__timber.log('TwitchWebsocketClient', f'Full dataBundle output: ({dataBundle=})')

        if exception is not None:
            self.__timber.log('TwitchWebsocketClient', f'Encountered an exception when attempting to convert dictionary into TwitchWebsocketDataBundle ({dataBundle=}) ({dictionary=}) ({message=}): {exception}', exception, traceback.format_exc())
            return None
        elif dataBundle is None:
            self.__timber.log('TwitchWebsocketClient', f'Received `None` when attempting to convert dictionary into TwitchWebsocketDataBundle ({dataBundle=}) ({dictionary=}) ({message=})')
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
        self.__backgroundTaskHelper.createTask(self.__startWebsocketConnection())
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

    async def __startWebsocketConnection(self):
        twitchWebsocketUrl = self.__twitchWebsocketUrl
        self.__timber.log('TwitchWebsocketClient', f'Connecting to websocket \"{twitchWebsocketUrl}\"...')

        try:
            async with websockets.connect(twitchWebsocketUrl) as websocket:
                async for message in websocket:
                    dataBundle = await self.__parseMessageToDataBundleFor(message)

                    if dataBundle is None or not await self.__isValidMessage(dataBundle):
                        continue

                    connectionAction = await self.__handleConnectionRelatedMessageFor(dataBundle)

                    match connectionAction:
                        case TwitchWebsocketClient.ConnectionAction.CREATE_EVENT_SUB_SUBSCRIPTION:
                            self.__timber.log('TwitchWebsocketClient', f'Twitch websocket connection is asking for EventSub subscription(s) to be created ({connectionAction=})')
                            await self.__createEventSubSubscription()

                        case TwitchWebsocketClient.ConnectionAction.DISCONNECT:
                            self.__timber.log('TwitchWebsocketClient', f'Twitch websocket connection was revoked when connected to \"{twitchWebsocketUrl=}\" ({connectionAction=})')
                            await websocket.close()

                        case TwitchWebsocketClient.ConnectionAction.OK:
                            # this path is intentionally empty
                            pass

                        case TwitchWebsocketClient.ConnectionAction.RECONNECT:
                            self.__timber.log('TwitchWebsocketClient', f'Twitch websocket connection is asking for a new connection to be made ({connectionAction=})')
                            self.__backgroundTaskHelper.createTask(self.__startWebsocketConnection())

                    await self.__submitDataBundle(dataBundle)
        except Exception as e:
            self.__timber.log('TwitchWebsocketClient', f'Encountered websocket exception when connected to \"{twitchWebsocketUrl}\": {e}', e, traceback.format_exc())

    async def __submitDataBundle(self, dataBundle: TwitchWebsocketDataBundle):
        if not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        try:
            self.__dataBundleQueue.put(dataBundle, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('TwitchWebsocketClient', f'Encountered queue.Full when submitting a new dataBundle ({dataBundle}) into the dataBundle queue (queue size: {self.__dataBundleQueue.qsize()}): {e}', e, traceback.format_exc())
