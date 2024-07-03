import asyncio
import json
import queue
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue
from typing import Any

import websockets

from .websocketConnectionServerInterface import WebsocketConnectionServerInterface
from .websocketEvent import WebsocketEvent
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..storage.jsonReaderInterface import JsonReaderInterface
from ..timber.timberInterface import TimberInterface


class WebsocketConnectionServer(WebsocketConnectionServerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        settingsJsonReader: JsonReaderInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        sleepTimeSeconds: float = 5,
        port: int = 8765,
        host: str = '0.0.0.0',
        websocketSettingsFile: str = 'websocketSettings.json',
        eventTimeToLive: timedelta = timedelta(seconds = 30)
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 3 or sleepTimeSeconds > 10:
            raise TypeError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(port):
            raise TypeError(f'port argument is malformed: \"{port}\"')
        elif port <= 1000 or port > utils.getIntMaxSafeSize():
            raise TypeError(f'port argument is out of bounds: {port}')
        elif not utils.isValidStr(host):
            raise TypeError(f'host argument is malformed: \"{host}\"')
        elif not utils.isValidStr(websocketSettingsFile):
            raise TypeError(f'websocketSettingsFile argument is malformed: \"{websocketSettingsFile}\"')
        elif not isinstance(eventTimeToLive, timedelta):
            raise TypeError(f'eventTimeToLive argument is malformed: \"{eventTimeToLive}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__port: int = port
        self.__host: str = host
        self.__websocketSettingsFile: str = websocketSettingsFile
        self.__eventTimeToLive: timedelta = eventTimeToLive

        self.__isStarted: bool = False
        self.__cache: dict[str, Any] | None = None
        self.__eventQueue: SimpleQueue[WebsocketEvent] = SimpleQueue()

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('WebsocketConnectionServer', 'Caches cleared')

    async def __isDebugLoggingEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'debugLoggingEnabled', False)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from Websocket settings file: \"{self.__websocketSettingsFile}\"')

        self.__cache = jsonContents
        return jsonContents

    async def sendEvent(
        self,
        twitchChannel: str,
        eventType: str,
        eventData: dict[Any, Any]
    ):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(eventType):
            raise ValueError(f'eventType argument for twitchChannel \"{twitchChannel}\" is malformed: \"{eventType}\"')
        elif not isinstance(eventData, dict) or len(eventData) == 0:
            raise ValueError(f'eventData argument for eventType \"{eventType}\" and twitchChannel \"{twitchChannel}\" is malformed: \"{eventData}\"')

        event: dict[str, Any] = {
            'twitchChannel': twitchChannel,
            'eventType': eventType,
            'eventData': eventData
        }

        if await self.__isDebugLoggingEnabled():
            currentSize = self.__eventQueue.qsize()
            self.__timber.log('WebsocketConnectionServer', f'Adding event to queue (current qsize is {currentSize}): {event}')

        self.__eventQueue.put(WebsocketEvent(
            eventTime = datetime.now(self.__timeZoneRepository.getDefault()), 
            eventData = event
        ))

    def start(self):
        if self.__isStarted:
            self.__timber.log('WebsocketConnectionServer', 'Not starting WebsocketConnectionServer as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('WebsocketConnectionServer', 'Starting WebsocketConnectionServer...')
        self.__backgroundTaskHelper.createTask(self.__startEventLoop())

    async def __startEventLoop(self):
        while True:
            try:
                async with websockets.serve(
                    self.__websocketConnectionReceived,
                    host = self.__host,
                    port = self.__port
                ) as websocket:
                    if await self.__isDebugLoggingEnabled():
                        self.__timber.log('WebsocketConnectionServer', f'Looping within `__start()`')

                    await websocket.wait_closed()
            except Exception as e:
                self.__timber.log('WebsocketConnectionServer', f'Encountered exception within `__start()`: {e}', e, traceback.format_exc())

                if str(e) == 'Event loop is closed':
                    # this annoying code provides us an escape from this infinite loop when using
                    # CTRL+C at the terminal to stop the bot
                    self.__timber.log('WebsocketConnectionServer', f'Breaking from `__start()` loop')
                    break

            if await self.__isDebugLoggingEnabled():
                self.__timber.log('WebsocketConnectionServer', f'Sleeping within `__start()`')

            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __websocketConnectionReceived(self, websocket, path):
        if await self.__isDebugLoggingEnabled():
            self.__timber.log('WebsocketConnectionServer', f'Entered `__websocketConnectionReceived()` (path: \"{path}\") (qsize: {self.__eventQueue.qsize()})')

        while websocket.open:
            while not self.__eventQueue.empty():
                isDebugLoggingEnabled = await self.__isDebugLoggingEnabled()

                try:
                    event = self.__eventQueue.get_nowait()

                    if event.eventTime + self.__eventTimeToLive >= datetime.now(self.__timeZoneRepository.getDefault()):
                        eventJson = json.dumps(event.eventData, sort_keys = True)
                        await websocket.send(eventJson)

                        if isDebugLoggingEnabled:
                            self.__timber.log('WebsocketConnectionServer', f'Sent event to \"{path}\": {event.eventData}')
                        else:
                            self.__timber.log('WebsocketConnectionServer', f'Sent event to \"{path}\"')
                    else:
                        if isDebugLoggingEnabled:
                            self.__timber.log('WebsocketConnectionServer', f'Discarded an event meant for \"{path}\": {event.eventData}')
                        else:
                            self.__timber.log('WebsocketConnectionServer', f'Discarded an event meant for \"{path}\"')
                except queue.Empty as e:
                    self.__timber.log('WebsocketConnectionServer', f'Encountered queue.Empty error when looping through events (qsize: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

        if await self.__isDebugLoggingEnabled():
            self.__timber.log('WebsocketConnectionServer', f'Exiting `__websocketConnectionReceived()`')
