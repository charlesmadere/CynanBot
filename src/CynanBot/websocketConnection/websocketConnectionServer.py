import asyncio
import json
import queue
import traceback
from datetime import datetime, timedelta, timezone
from queue import SimpleQueue
from typing import Any, Dict, Optional

import websockets

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface
from CynanBot.websocketConnection.websocketEvent import WebsocketEvent


class WebsocketConnectionServer(WebsocketConnectionServerInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        settingsJsonReader: JsonReaderInterface,
        timber: TimberInterface,
        sleepTimeSeconds: float = 5,
        port: int = 8765,
        host: str = '0.0.0.0',
        websocketSettingsFile: str = 'websocketSettings.json',
        eventTimeToLive: timedelta = timedelta(seconds = 30),
        timeZone: timezone = timezone.utc
    ):
        assert isinstance(backgroundTaskHelper, BackgroundTaskHelper), f"malformed {backgroundTaskHelper=}"
        assert isinstance(settingsJsonReader, JsonReaderInterface), f"malformed {settingsJsonReader=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        if not utils.isValidNum(sleepTimeSeconds):
            raise ValueError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        if sleepTimeSeconds < 3 or sleepTimeSeconds > 10:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        if not utils.isValidInt(port):
            raise ValueError(f'port argument is malformed: \"{port}\"')
        if port <= 1000 or port > utils.getIntMaxSafeSize():
            raise ValueError(f'port argument is out of bounds: {port}')
        if not utils.isValidStr(host):
            raise ValueError(f'host argument is malformed: \"{host}\"')
        if not utils.isValidStr(websocketSettingsFile):
            raise ValueError(f'websocketSettingsFile argument is malformed: \"{websocketSettingsFile}\"')
        assert isinstance(eventTimeToLive, timedelta), f"malformed {eventTimeToLive=}"
        assert isinstance(timeZone, timezone), f"malformed {timeZone=}"

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__timber: TimberInterface = timber
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__port: int = port
        self.__host: str = host
        self.__websocketSettingsFile: str = websocketSettingsFile
        self.__eventTimeToLive: timedelta = eventTimeToLive
        self.__timeZone: timezone = timeZone

        self.__isStarted: bool = False
        self.__cache: Optional[Dict[str, Any]] = None
        self.__eventQueue: SimpleQueue[WebsocketEvent] = SimpleQueue()

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('WebsocketConnectionServer', 'Caches cleared')

    async def __isDebugLoggingEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'debugLoggingEnabled', False)

    async def __readJson(self) -> Dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: Optional[Dict[str, Any]] = None

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
        eventData: Dict[Any, Any]
    ):
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        if not utils.isValidStr(eventType):
            raise ValueError(f'eventType argument for twitchChannel \"{twitchChannel}\" is malformed: \"{eventType}\"')
        if not isinstance(eventData, Dict) or len(eventData) == 0:
            raise ValueError(f'eventData argument for eventType \"{eventType}\" and twitchChannel \"{twitchChannel}\" is malformed: \"{eventData}\"')

        event: Dict[str, Any] = {
            'twitchChannel': twitchChannel,
            'eventType': eventType,
            'eventData': eventData
        }

        if await self.__isDebugLoggingEnabled():
            currentSize = self.__eventQueue.qsize()
            self.__timber.log('WebsocketConnectionServer', f'Adding event to queue (current qsize is {currentSize}): {event}')

        self.__eventQueue.put(WebsocketEvent(
            eventData = event,
            timeZone = self.__timeZone
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

                    if event.getEventTime() + self.__eventTimeToLive >= datetime.now(self.__timeZone):
                        eventJson = json.dumps(event.getEventData(), sort_keys = True)
                        await websocket.send(eventJson)

                        if isDebugLoggingEnabled:
                            self.__timber.log('WebsocketConnectionServer', f'Sent event to \"{path}\": {event.getEventData()}')
                        else:
                            self.__timber.log('WebsocketConnectionServer', f'Sent event to \"{path}\"')
                    else:
                        if isDebugLoggingEnabled:
                            self.__timber.log('WebsocketConnectionServer', f'Discarded an event meant for \"{path}\": {event.getEventData()}')
                        else:
                            self.__timber.log('WebsocketConnectionServer', f'Discarded an event meant for \"{path}\"')
                except queue.Empty as e:
                    self.__timber.log('WebsocketConnectionServer', f'Encountered queue.Empty error when looping through events (qsize: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__sleepTimeSeconds)

        if await self.__isDebugLoggingEnabled():
            self.__timber.log('WebsocketConnectionServer', f'Exiting `__websocketConnectionReceived()`')
