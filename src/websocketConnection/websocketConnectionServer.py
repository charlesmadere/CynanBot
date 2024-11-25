import asyncio
import json
import queue
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue
from typing import Any

import websockets
from websockets.asyncio.server import ServerConnection

from .mapper.websocketEventTypeMapperInterface import WebsocketEventTypeMapperInterface
from .settings.websocketConnectionServerSettingsInterface import WebsocketConnectionServerSettingsInterface
from .websocketConnectionServerInterface import WebsocketConnectionServerInterface
from .websocketEvent import WebsocketEvent
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
        queueTimeoutSeconds: int = 3
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

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__websocketConnectionServerSettings: WebsocketConnectionServerSettingsInterface = websocketConnectionServerSettings
        self.__websocketEventTypeMapper: WebsocketEventTypeMapperInterface = websocketEventTypeMapper
        self.__websocketSleepTimeSeconds: float = websocketSleepTimeSeconds
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds

        self.__isStarted: bool = False
        self.__eventQueue: SimpleQueue[WebsocketEvent] = SimpleQueue()

    async def __serializeEventToJson(self, event: WebsocketEvent) -> str:
        if not isinstance(event, WebsocketEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        # TODO will add more logic here in the future
        return json.dumps(event.eventData, sort_keys = True)

    def start(self):
        if self.__isStarted:
            self.__timber.log('WebsocketConnectionServer', 'Not starting WebsocketConnectionServer as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('WebsocketConnectionServer', 'Starting WebsocketConnectionServer...')
        self.__backgroundTaskHelper.createTask(self.__startWebsocketServer())

    async def __startWebsocketServer(self):
        while True:
            host = await self.__websocketConnectionServerSettings.getHost()
            port = await self.__websocketConnectionServerSettings.getPort()

            try:
                async with websockets.serve(
                    self.__websocketConnectionReceived,
                    host = host,
                    port = port
                ) as websocket:
                    self.__timber.log('WebsocketConnectionServer', f'Serving in progress... ({host=}) ({port=})')
                    await websocket.wait_closed()
            except Exception as e:
                self.__timber.log('WebsocketConnectionServer', f'Encountered exception within `__startWebsocketServer()` ({host=}) ({port=}): {e}', e, traceback.format_exc())

                if str(e) == 'Event loop is closed':
                    # this annoying code provides us an escape from this infinite loop when using
                    # CTRL+C at the terminal to stop the bot
                    self.__timber.log('WebsocketConnectionServer', f'Breaking from `__startWebsocketServer()` loop')
                    return

            self.__timber.log('WebsocketConnectionServer', f'Sleeping within `__startWebsocketServer()`')
            await asyncio.sleep(self.__websocketSleepTimeSeconds)

    def submitEvent(
        self,
        twitchChannel: str,
        eventType: str,
        eventData: dict[str, Any]
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(eventType):
            raise TypeError(f'eventType argument for twitchChannel \"{twitchChannel}\" is malformed: \"{eventType}\"')
        elif not isinstance(eventData, dict) or len(eventData) == 0:
            raise TypeError(f'eventData argument for eventType \"{eventType}\" and twitchChannel \"{twitchChannel}\" is malformed: \"{eventData}\"')

        event: dict[str, Any] = {
            'twitchChannel': twitchChannel,
            'eventType': eventType,
            'eventData': eventData
        }

        websocketEvent = WebsocketEvent(
            eventTime = datetime.now(self.__timeZoneRepository.getDefault()), 
            eventData = event
        )

        try:
            self.__eventQueue.put(websocketEvent, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('WebsocketConnectionServer', f'Encountered queue.Full when submitting a new event ({websocketEvent=}) into the event queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())

    async def __websocketConnectionReceived(
        self,
        serverConnection: ServerConnection
    ):
        self.__timber.log('WebsocketConnectionServer', f'Entered `__websocketConnectionReceived()` ({serverConnection=}) (qsize: {self.__eventQueue.qsize()})')

        while await serverConnection.wait_closed():
            eventTimeToLive = timedelta(
                seconds = await self.__websocketConnectionServerSettings.getEventTimeToLiveSeconds()
            )

            events: list[WebsocketEvent] = list()

            try:
                while not self.__eventQueue.empty():
                    events.append(self.__eventQueue.get_nowait())
            except queue.Empty as e:
                self.__timber.log('WebsocketConnectionServer', f'Encountered queue.Empty error when looping through events ({serverConnection=}) (qsize: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())

            if len(events) >= 1:
                now = datetime.now(self.__timeZoneRepository.getDefault())

                for event in events:
                    if event.eventTime + eventTimeToLive >= now:
                        eventJson = await self.__serializeEventToJson(event)
                        await serverConnection.send(eventJson)
                        self.__timber.log('WebsocketConnectionServer', f'Sent websocket event ({serverConnection=}) ({event=})')
                    else:
                        self.__timber.log('WebsocketConnectionServer', f'Discarded websocket event ({serverConnection=}) ({event=})')

            await asyncio.sleep(self.__websocketSleepTimeSeconds)

        self.__timber.log('WebsocketConnectionServer', f'Exiting `__websocketConnectionReceived()` ({serverConnection=})')
