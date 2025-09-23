import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Final

from bleak import BleakClient, BleakScanner, BLEDevice
from frozenlist import FrozenList

from .pixelsDiceMachineInterface import PixelsDiceMachineInterface
from ..listeners.pixelsDiceEventListener import PixelsDiceEventListener
from ..models.diceBluetoothInfo import DiceBluetoothInfo
from ..models.events.absPixelsDiceEvent import AbsPixelsDiceEvent
from ..models.events.pixelsDiceClientDisconnectedEvent import PixelsDiceClientDisconnectedEvent
from ..pixelsDiceSettingsInterface import PixelsDiceSettingsInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class PixelsDiceMachine(PixelsDiceMachineInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        pixelsDiceSettings: PixelsDiceSettingsInterface,
        timber: TimberInterface,
        connectionLoopSleepTimeSeconds: float = 10,
        eventLoopSleepTimeSeconds: float = 0.5,
        queueTimeoutSeconds: int = 3,
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(pixelsDiceSettings, PixelsDiceSettingsInterface):
            raise TypeError(f'pixelsDiceSettings argument is malformed: \"{pixelsDiceSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(connectionLoopSleepTimeSeconds):
            raise TypeError(f'connectionLoopSleepTimeSeconds argument is malformed: \"{connectionLoopSleepTimeSeconds}\"')
        elif connectionLoopSleepTimeSeconds < 3 or connectionLoopSleepTimeSeconds > 60:
            raise ValueError(f'connectionLoopSleepTimeSeconds argument is out of bounds: {connectionLoopSleepTimeSeconds}')
        elif not utils.isValidNum(eventLoopSleepTimeSeconds):
            raise TypeError(f'eventLoopSleepTimeSeconds argument is malformed: \"{eventLoopSleepTimeSeconds}\"')
        elif eventLoopSleepTimeSeconds < 0.25 or eventLoopSleepTimeSeconds > 3:
            raise ValueError(f'eventLoopSleepTimeSeconds argument is out of bounds: {eventLoopSleepTimeSeconds}')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__pixelsDiceSettings: Final[PixelsDiceSettingsInterface] = pixelsDiceSettings
        self.__timber: Final[TimberInterface] = timber
        self.__connectionLoopSleepTimeSeconds: Final[float] = connectionLoopSleepTimeSeconds
        self.__eventLoopSleepTimeSeconds: Final[float] = eventLoopSleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds

        self.__eventQueue: Final[SimpleQueue[AbsPixelsDiceEvent]] = SimpleQueue()

        self.__isStarted: bool = False
        self.__connectedDice: DiceBluetoothInfo | None = None
        self.__eventListener: PixelsDiceEventListener | None = None

    async def __connectToDice(self) -> DiceBluetoothInfo | None:
        diceName = await self.__pixelsDiceSettings.getDiceName()

        if not utils.isValidStr(diceName):
            self.__timber.log('PixelsDiceMachine', f'No dice name available to scan for ({diceName=})')
            return None

        try:
            devices = await BleakScanner.discover()
        except Exception as e:
            self.__timber.log('PixelsDiceMachine', f'Failed to scan for devices', e, traceback.format_exc())
            return None

        diceDevice: BLEDevice | None = None
        connectedDice: DiceBluetoothInfo | None = None
        allDeviceNames: set[str] = set()

        for index, device in enumerate(devices):
            if not utils.isValidStr(device.name):
                continue

            allDeviceNames.add(device.name)

            if diceDevice is None and device.name.casefold() == diceName.casefold():
                diceDevice = device

                connectedDice = DiceBluetoothInfo(
                    diceAddress = device.address,
                    diceName = device.name,
                )

        if not isinstance(diceDevice, BLEDevice) or connectedDice is None:
            self.__timber.log('PixelsDiceMachine', f'Failed to find device with name \"{diceName}\" among {len(devices)} device(s): {allDeviceNames=}')
            return None

        self.__timber.log('PixelsDiceMachine', f'Found device ({connectedDice=}) among {len(devices)} device(s)')

        client = BleakClient(
            address_or_ble_device = diceDevice,
            disconnected_callback = self.__onBleakClientDisconnected,
        )

        try:
            await client.connect()
        except Exception as e:
            self.__timber.log('PixelsDiceMachine', f'Failed to establish a connection ({connectedDice=}) ({client=})', e, traceback.format_exc())
        finally:
            await client.disconnect()

        return connectedDice

    def __onBleakClientDisconnected(self, client: BleakClient):
        previouslyConnectedDice = self.__connectedDice
        self.__connectedDice = None

        self.__timber.log('PixelsDiceMachine', f'Pixels Dice disconnected ({client=}) ({previouslyConnectedDice=})')

        self.__submitEvent(PixelsDiceClientDisconnectedEvent(
            previouslyConnectedDice = previouslyConnectedDice,
        ))

    def setEventListener(self, listener: PixelsDiceEventListener | None):
        if listener is not None and not isinstance(listener, PixelsDiceEventListener):
            raise TypeError(f'listener argument is malformed: \"{listener}\"')

        self.__eventListener = listener

    def start(self):
        if self.__isStarted:
            self.__timber.log('PixelsDiceMachine', 'Not starting PixelsDiceMachine as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('PixelsDiceMachine', 'Starting PixelsDiceMachine...')
        self.__backgroundTaskHelper.createTask(self.__startConnectionLoop())
        self.__backgroundTaskHelper.createTask(self.__startEventLoop())

    async def __startConnectionLoop(self):
        while True:
            connectedDice = self.__connectedDice

            if connectedDice is None:
                connectedDice = await self.__connectToDice()
                self.__connectedDice = connectedDice

            await asyncio.sleep(self.__connectionLoopSleepTimeSeconds)

    async def __startEventLoop(self):
        while True:
            eventListener = self.__eventListener

            if eventListener is not None:
                events: FrozenList[AbsPixelsDiceEvent] = FrozenList()

                try:
                    while not self.__eventQueue.empty():
                        event = self.__eventQueue.get_nowait()
                        events.append(event)
                except queue.Empty as e:
                    self.__timber.log('PixelsDiceMachine', f'Encountered queue.Empty when building up events list (queue size: {self.__eventQueue.qsize()}) ({len(events)=}) ({events=}): {e}', e, traceback.format_exc())

                events.freeze()

                for index, event in enumerate(events):
                    try:
                        await eventListener.onNewPixelsDiceEvent(event)
                    except Exception as e:
                        self.__timber.log('PixelsDiceMachine', f'Encountered unknown Exception when looping through events (queue size: {self.__eventQueue.qsize()}) ({len(events)=}) ({index=}) ({event=}): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__eventLoopSleepTimeSeconds)

    def __submitEvent(self, event: AbsPixelsDiceEvent):
        if not isinstance(event, AbsPixelsDiceEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        try:
            self.__eventQueue.put(event, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('PixelsDiceMachine', f'Encountered queue.Full when submitting a new event ({event}) into the event queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())

    async def test(self):
        connectedDice = await self.__connectToDice()
        print(f'{connectedDice=}')
