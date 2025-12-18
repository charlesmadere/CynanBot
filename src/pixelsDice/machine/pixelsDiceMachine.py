import asyncio
import queue
import traceback
from queue import SimpleQueue
from typing import Any, Final

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from frozenlist import FrozenList

from .pixelsDiceMachineInterface import PixelsDiceMachineInterface
from ..exceptions import PixelsDiceRequestQueueException
from ..listeners.pixelsDiceEventListener import PixelsDiceEventListener
from ..mappers.pixelsDiceStateMapperInterface import PixelsDiceStateMapperInterface
from ..models.diceBluetoothInfo import DiceBluetoothInfo
from ..models.diceRollRequest import DiceRollRequest
from ..models.diceRollResult import DiceRollResult
from ..models.events.absPixelsDiceEvent import AbsPixelsDiceEvent
from ..models.events.pixelsDiceClientConnectedEvent import PixelsDiceClientConnectedEvent
from ..models.events.pixelsDiceClientDisconnectedEvent import PixelsDiceClientDisconnectedEvent
from ..models.events.pixelsDiceRollEvent import PixelsDiceRollEvent
from ..models.states.pixelsDiceRollState import PixelsDiceRollState
from ..pixelsDiceSettingsInterface import PixelsDiceSettingsInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class PixelsDiceMachine(PixelsDiceMachineInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        pixelsDiceStateMapper: PixelsDiceStateMapperInterface,
        pixelsDiceSettings: PixelsDiceSettingsInterface,
        timber: TimberInterface,
        connectionLoopSleepTimeSeconds: float = 10,
        eventLoopSleepTimeSeconds: float = 0.5,
        queueTimeoutSeconds: int = 3,
        notifyCharacteristicUuid: str = '6e400001-b5a3-f393-e0a9-e50e24dcca9e',
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(pixelsDiceStateMapper, PixelsDiceStateMapperInterface):
            raise TypeError(f'pixelsDiceStateMapper argument is malformed: \"{pixelsDiceStateMapper}\"')
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
        elif not utils.isValidStr(notifyCharacteristicUuid):
            raise TypeError(f'notifyCharacteristicUuid argument is malformed: \"{notifyCharacteristicUuid}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__pixelsDiceStateMapper: Final[PixelsDiceStateMapperInterface] = pixelsDiceStateMapper
        self.__pixelsDiceSettings: Final[PixelsDiceSettingsInterface] = pixelsDiceSettings
        self.__timber: Final[TimberInterface] = timber
        self.__connectionLoopSleepTimeSeconds: Final[float] = connectionLoopSleepTimeSeconds
        self.__eventLoopSleepTimeSeconds: Final[float] = eventLoopSleepTimeSeconds
        self.__queueTimeoutSeconds: Final[int] = queueTimeoutSeconds
        self.__notifyCharacteristicUuid: Final[str] = notifyCharacteristicUuid

        self.__eventQueue: Final[SimpleQueue[AbsPixelsDiceEvent]] = SimpleQueue()
        self.__requestQueue: Final[SimpleQueue[DiceRollRequest]] = SimpleQueue()

        self.__isStarted: bool = False
        self.__connectedDice: DiceBluetoothInfo | None = None
        self.__eventListener: PixelsDiceEventListener | None = None

    async def __connectToDice(self) -> DiceBluetoothInfo | None:
        if not await self.__pixelsDiceSettings.isEnabled():
            return None

        diceName = await self.__pixelsDiceSettings.getDiceName()

        if not utils.isValidStr(diceName):
            self.__timber.log('PixelsDiceMachine', f'No dice name available to scan for ({diceName=})')
            return None

        try:
            devices = await BleakScanner.discover(
                return_adv = True,
                service_uuids = [ self.__notifyCharacteristicUuid ],
            )
        except Exception as e:
            self.__timber.log('PixelsDiceMachine', f'Failed to scan for devices', e, traceback.format_exc())
            return None

        diceDevice: BLEDevice | Any | None = None
        diceAdvertisement: AdvertisementData | None = None
        connectedDice: DiceBluetoothInfo | None = None
        allDeviceNames: set[str] = set()

        for device, advertisement in devices.values():
            if not utils.isValidStr(device.name):
                continue

            allDeviceNames.add(device.name)

            if diceDevice is None and device.name.casefold() == diceName.casefold():
                diceDevice = device
                diceAdvertisement = advertisement

                connectedDice = DiceBluetoothInfo(
                    diceAddress = device.address,
                    diceName = device.name,
                )

        if not isinstance(diceDevice, BLEDevice) or not isinstance(diceAdvertisement, AdvertisementData) or connectedDice is None:
            self.__timber.log('PixelsDiceMachine', f'Failed to find device with name \"{diceName}\" among {len(devices)} device(s): {allDeviceNames}')
            return None

        self.__timber.log('PixelsDiceMachine', f'Found device ({diceName=}) ({connectedDice=}) ({diceDevice=}) ({diceAdvertisement=})')

        client = BleakClient(
            address_or_ble_device = diceDevice,
            disconnected_callback = self.__onBleakClientDisconnected,
            services = [ self.__notifyCharacteristicUuid ],
        )

        try:
            await client.connect()
        except Exception as e:
            self.__timber.log('PixelsDiceMachine', f'Failed to establish a connection ({connectedDice=}) ({client=})', e, traceback.format_exc())
            return None

        notifyCharacteristic = client.services.get_characteristic(self.__notifyCharacteristicUuid)

        if not isinstance(notifyCharacteristic, BleakGATTCharacteristic):
            self.__timber.log('PixelsDiceMachine', f'Failed to retrieve notify characteristic ({notifyCharacteristic=}) ({connectedDice=}) ({client=})')
            await client.disconnect()
            return None

        await self.__submitEvent(PixelsDiceClientConnectedEvent(
            connectedDice = connectedDice,
        ))

        await client.start_notify(
            char_specifier = notifyCharacteristic,
            callback = self.__onBleakClientNotify,
        )

        return connectedDice

    @property
    def isConnected(self) -> bool:
        return self.__connectedDice is not None

    def __onBleakClientDisconnected(self, client: BleakClient):
        self.__backgroundTaskHelper.createTask(self.__onBleakClientDisconnectedAsync(
            client = client,
        ))

    async def __onBleakClientDisconnectedAsync(self, client: BleakClient):
        previouslyConnectedDice = self.__connectedDice
        self.__connectedDice = None

        self.__timber.log('PixelsDiceMachine', f'Pixels Dice disconnected ({client=}) ({previouslyConnectedDice=})')

        await self.__submitEvent(PixelsDiceClientDisconnectedEvent(
            previouslyConnectedDice = previouslyConnectedDice,
        ))

    async def __onBleakClientNotify(
        self,
        characteristic: BleakGATTCharacteristic,
        rawData: bytearray,
    ):
        if characteristic.uuid != self.__notifyCharacteristicUuid:
            self.__timber.log('PixelsDiceMachine', f'Received a characteristic notification with the wrong UUID ({characteristic=})')
            return

        connectedDice = self.__connectedDice

        if connectedDice is None:
            self.__timber.log('PixelsDiceMachine', f'Received a characteristic notification, but there is no connected dice ({connectedDice=}) ({characteristic=})')
            return

        state = await self.__pixelsDiceStateMapper.map(
            rawData = rawData,
        )

        if isinstance(state, PixelsDiceRollState):
            await self.__submitEvent(PixelsDiceRollEvent(
                connectedDice = connectedDice,
                roll = state.roll,
            ))

        else:
            # empty for now, but in the future, we may want to observe other states
            pass

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
                    self.__timber.log('PixelsDiceMachine', f'Encountered queue.Empty when building up events list (queue size: {self.__eventQueue.qsize()}) ({len(events)=}) ({events=})', e, traceback.format_exc())

                events.freeze()

                for index, event in enumerate(events):
                    try:
                        await eventListener.onNewPixelsDiceEvent(event)
                    except Exception as e:
                        self.__timber.log('PixelsDiceMachine', f'Encountered unknown Exception when looping through events (queue size: {self.__eventQueue.qsize()}) ({len(events)=}) ({index=}) ({event=})', e, traceback.format_exc())

                    if not isinstance(event, PixelsDiceRollEvent):
                        continue

                    request: DiceRollRequest | None = None

                    if not self.__requestQueue.empty():
                        try:
                            request = self.__requestQueue.get_nowait()
                        except queue.Empty as e:
                            self.__timber.log('PixelsDiceMachine', f'Encountered queue.Empty when retrieving a dice roll request (queue size: {self.__requestQueue.qsize()}) ({len(events)=}) ({index=}) ({event=})', e, traceback.format_exc())

                    if request is None:
                        continue

                    result = DiceRollResult(
                        remainingQueueSize = self.__requestQueue.qsize(),
                        roll = event.roll,
                    )

                    try:
                        await request.callback(result)
                    except Exception as e:
                        self.__timber.log('PixelsDiceMachine', f'Encountered unknown Exception when notifying pixel dice roll (queue size: {self.__requestQueue.qsize()}) ({len(events)=}) ({index=}) ({event=}) ({request=})', e, traceback.format_exc())

            await asyncio.sleep(self.__eventLoopSleepTimeSeconds)

    async def __submitEvent(self, event: AbsPixelsDiceEvent):
        if not isinstance(event, AbsPixelsDiceEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        try:
            self.__eventQueue.put(event, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('PixelsDiceMachine', f'Encountered queue.Full when submitting a new event ({event}) into the event queue (queue size: {self.__eventQueue.qsize()})', e, traceback.format_exc())

    def submitRequest(self, request: DiceRollRequest) -> int:
        if not isinstance(request, DiceRollRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        try:
            self.__requestQueue.put(request, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('PixelsDiceMachine', f'Encountered queue.Full when submitting a new request ({request}) into the request queue (queue size: {self.__requestQueue.qsize()})', e, traceback.format_exc())
            raise PixelsDiceRequestQueueException(f'Failed to add a new request ({request}) into the request queue (queue size: {self.__requestQueue.qsize()})')

        return self.__requestQueue.qsize()
