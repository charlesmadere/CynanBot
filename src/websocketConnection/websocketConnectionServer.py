import asyncio
import json
import queue
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue
from typing import Any, Final

import websockets
from frozenlist import FrozenList
from websockets.asyncio.server import ServerConnection

from .mapper.websocketEventTypeMapperInterface import WebsocketEventTypeMapperInterface
from .settings.websocketConnectionServerSettingsInterface import WebsocketConnectionServerSettingsInterface
from .websocketConnectionServerInterface import WebsocketConnectionServerInterface
from .websocketEvent import WebsocketEvent
from .websocketEventType import WebsocketEventType
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface


class WebsocketConnectionServer(WebsocketConnectionServerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        websocketConnectionServerSettings: WebsocketConnectionServerSettingsInterface,
        websocketEventTypeMapper: WebsocketEventTypeMapperInterface,
        websocketSleepTimeSeconds: float = 3,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(websocketConnectionServerSettings, WebsocketConnectionServerSettingsInterface):
            raise TypeError(f'websocketConnectionServerSettings argument is malformed: \"{websocketConnectionServerSettings}\"')
        elif not isinstance(websocketEventTypeMapper, WebsocketEventTypeMapperInterface):
            raise TypeError(f'websocketEventTypeMapper argument is malformed: \"{websocketEventTypeMapper}\"')
        elif not utils.isValidNum(websocketSleepTimeSeconds):
            raise TypeError(f'websocketSleepTimeSeconds argument is malformed: \"{websocketSleepTimeSeconds}\"')
        elif websocketSleepTimeSeconds < 3 or websocketSleepTimeSeconds > 10:
            raise TypeError(f'websocketSleepTimeSeconds argument is out of bounds: {websocketSleepTimeSeconds}')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__websocketConnectionServerSettings: Final[WebsocketConnectionServerSettingsInterface] = websocketConnectionServerSettings
        self.__websocketEventTypeMapper: Final[WebsocketEventTypeMapperInterface] = websocketEventTypeMapper
        self.__websocketSleepTimeSeconds: Final[float] = websocketSleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__eventQueue: Final[SimpleQueue[WebsocketEvent]] = SimpleQueue()

    async def __handleWebsocketEvents(
        self,
        events: FrozenList[WebsocketEvent],
        serverConnection: ServerConnection,
    ):
        if len(events) == 0:
            return

        eventTimeToLive = timedelta(
            seconds = await self.__websocketConnectionServerSettings.getEventTimeToLiveSeconds(),
        )

        now = datetime.now(self.__timeZoneRepository.getDefault())

        for index, event in enumerate(events):
            if event.eventTime + eventTimeToLive >= now:
                eventJson = await self.__serializeEventToJson(event)

                try:
                    await serverConnection.send(eventJson)
                    self.__timber.log('WebsocketConnectionServer', f'Successfully sent websocket event ({serverConnection=}) ({event=}) ({index=})')
                except Exception as e:
                    self.__timber.log('WebsocketConnectionServer', f'Failed to send websocket event ({serverConnection=}) ({event=}) ({index=})', e, traceback.format_exc())
            else:
                self.__timber.log('WebsocketConnectionServer', f'Discarded websocket event as it is too old ({serverConnection=}) ({event=}) ({index=})')

    async def __serializeEventToJson(self, event: WebsocketEvent) -> str:
        if not isinstance(event, WebsocketEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        # may need to add more logic here in the future if there are ever more event types
        return json.dumps(event.eventData, sort_keys = True)

    def start(self):
        if self.__isStarted:
            self.__timber.log('WebsocketConnectionServer', 'Not starting WebsocketConnectionServer as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('WebsocketConnectionServer', 'Starting WebsocketConnectionServer...')
        self.__backgroundTaskHelper.createTask(self.__startServerLoop())

    async def __startServerLoop(self):
        while True:
            host = await self.__websocketConnectionServerSettings.getHost()
            port = await self.__websocketConnectionServerSettings.getPort()

            try:
                self.__timber.log('WebsocketConnectionServer', f'Starting connection... ({host=}) ({port=})')

                async with websockets.serve(
                    handler = self.__websocketConnectionReceived,
                    host = host,
                    port = port,
                ) as websocket:
                    await websocket.wait_closed()
            except Exception as e:
                if str(e) == 'Event loop is closed':
                    # this annoying code provides us an escape from this infinite loop when using
                    # CTRL+C at the terminal to stop the bot
                    return

                self.__timber.log('WebsocketConnectionServer', f'Encountered exception during server loop ({host=}) ({port=})', e, traceback.format_exc())

            await asyncio.sleep(self.__websocketSleepTimeSeconds)

    def submitEvent(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        eventType: WebsocketEventType,
        eventData: dict[str, Any],
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(eventType, WebsocketEventType):
            raise TypeError(f'eventType argument is malformed: \"{eventType}\"')
        elif not isinstance(eventData, dict):
            raise TypeError(f'eventData argument for eventType \"{eventType}\" and twitchChannel \"{twitchChannel}\" is malformed: \"{eventData}\"')

        if len(eventData) == 0:
            return

        event: dict[str, Any] = {
            'twitchChannel': twitchChannel,
            'twitchChannelId': twitchChannelId,
            'eventType': self.__websocketEventTypeMapper.toString(eventType),
            'eventData': eventData,
        }

        websocketEvent = WebsocketEvent(
            eventTime = datetime.now(self.__timeZoneRepository.getDefault()),
            eventData = event,
            eventType = eventType,
        )

        try:
            self.__eventQueue.put(websocketEvent, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('WebsocketConnectionServer', f'Encountered queue.Full when submitting a new event ({websocketEvent=}) into the event queue (queue size: {self.__eventQueue.qsize()})', e, traceback.format_exc())

    async def __websocketConnectionReceived(
        self,
        serverConnection: ServerConnection,
    ):
        if not isinstance(serverConnection, ServerConnection):
            raise TypeError(f'serverConnection argument is malformed: \"{serverConnection}\"')

        self.__timber.log('WebsocketConnectionServer', f'Entered `__websocketConnectionReceived()` ({serverConnection=}) (qsize: {self.__eventQueue.qsize()})')

        while True:
            events: FrozenList[WebsocketEvent] = FrozenList()

            try:
                while not self.__eventQueue.empty():
                    event = self.__eventQueue.get_nowait()
                    events.append(event)
            except queue.Empty as e:
                self.__timber.log('WebsocketConnectionServer', f'Encountered queue.Empty error when looping through events ({serverConnection=}) (qsize: {self.__eventQueue.qsize()})', e, traceback.format_exc())

            events.freeze()

            await self.__handleWebsocketEvents(
                events = events,
                serverConnection = serverConnection,
            )

            await asyncio.sleep(self.__websocketSleepTimeSeconds)
