import asyncio
import struct
import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Final

import psutil
import pywintypes
import win32file

from .bizhawkKey import BizhawkKey
from .bizhawkSettingsRepositoryInterface import BizhawkSettingsRepositoryInterface
from .exceptions import BizhawkProcessCantBeConnectedTo, BizhawkProcessNotFoundException
from ..actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ..actions.crowdControlAction import CrowdControlAction
from ..actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..crowdControlActionHandleResult import CrowdControlActionHandleResult
from ..crowdControlActionHandler import CrowdControlActionHandler
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface


class BizhawkActionHandler(CrowdControlActionHandler):

    @dataclass(frozen = True)
    class BizhawkConnection:
        connection: Any
        processId: int
        name: str

    @dataclass(frozen = True)
    class BizhawkProcessInfo:
        processId: int
        name: str

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        bizhawkSettingsRepository: BizhawkSettingsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        keyPressDelayFrames: int = 2,
        processConnectionCheckSleepTimeSeconds: int = 60,
        processConnectionTimeToLive: timedelta = timedelta(minutes = 15)
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(bizhawkSettingsRepository, BizhawkSettingsRepositoryInterface):
            raise TypeError(f'bizhawkSettingsRepository argument is malformed: \"{bizhawkSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(keyPressDelayFrames):
            raise TypeError(f'keyPressDelayMillis argument is malformed: \"{keyPressDelayFrames}\"')
        elif keyPressDelayFrames < 1 or keyPressDelayFrames > 8:
            raise ValueError(f'keyPressDelayFrames argument is out of bounds: {keyPressDelayFrames}')
        elif not utils.isValidInt(processConnectionCheckSleepTimeSeconds):
            raise TypeError(f'processConnectionCheckSleepTimeSeconds argument is malformed: \"{processConnectionCheckSleepTimeSeconds}\"')
        elif processConnectionCheckSleepTimeSeconds < 30 or processConnectionCheckSleepTimeSeconds > 1800:
            raise ValueError(f'processConnectionCheckSleepTimeSeconds argument is out of bounds: {processConnectionCheckSleepTimeSeconds}')
        elif not isinstance(processConnectionTimeToLive, timedelta):
            raise TypeError(f'processConnectionTimeToLive argument is malformed: \"{processConnectionTimeToLive}\"')

        self.__backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = backgroundTaskHelper
        self.__bizhawkSettingsRepository: Final[BizhawkSettingsRepositoryInterface] = bizhawkSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__processConnectionCheckSleepTimeSeconds: Final[float] = processConnectionCheckSleepTimeSeconds
        self.__keyPressDelayFrames: Final[int] = keyPressDelayFrames
        self.__processConnectionTimeToLive: Final[timedelta] = processConnectionTimeToLive

        self.__bizhawkConnection: BizhawkActionHandler.BizhawkConnection | None = None
        self.__isStarted: bool = False
        self.__lastBizhawkInputDateTime: datetime | None = None

    async def __closeConnectionIfUnused(self):
        bizhawkConnection = self.__bizhawkConnection
        lastBizhawkInputDateTime = self.__lastBizhawkInputDateTime

        if bizhawkConnection is None or lastBizhawkInputDateTime is None:
            return

        now = datetime.now(self.__timeZoneRepository.getDefault())

        if now - lastBizhawkInputDateTime < self.__processConnectionTimeToLive:
            return

        bizhawkConnection.connection.close()
        self.__bizhawkConnection = None
        self.__lastBizhawkInputDateTime = None
        self.__timber.log('BizhawkActionHandler', f'Closed Bizhawk connection as it hasn\'t recently been used ({bizhawkConnection=}) ({lastBizhawkInputDateTime=})')

    async def __convertDelayFramesToSeconds(self) -> float:
        return float(self.__keyPressDelayFrames) * float(0.0166666666666667)

    async def __findBizhawkProcessInfo(self) -> BizhawkProcessInfo | None:
        bizhawkProcessName = await self.__bizhawkSettingsRepository.getProcessName()
        bizhawkProcessInfo: BizhawkActionHandler.BizhawkProcessInfo | None = None

        try:
            for proc in psutil.process_iter(['name', 'pid']):
                processId: int | Any | None = proc.info.get('pid', None)
                processName: str | Any | None = proc.info.get('name', None)

                if not utils.isValidInt(processId) or not utils.isValidStr(processName):
                    continue
                elif bizhawkProcessName not in processName:
                    continue

                return BizhawkActionHandler.BizhawkProcessInfo(
                    processId = processId,
                    name = processName
                )
        except Exception as e:
            self.__timber.log('BizhawkActionHandler', f'Encountered exception when looping through available processes ({bizhawkProcessName=}) ({bizhawkProcessInfo=}): {e}', e, traceback.format_exc())

        self.__timber.log('BizhawkActionHandler', f'Failed to find any suitable Bizhawk process! ({bizhawkProcessName=}) ({bizhawkProcessInfo=})')
        return None

    async def __handleBizhawkKeyPress(
        self,
        keyBind: BizhawkKey,
        action: CrowdControlAction
    ) -> CrowdControlActionHandleResult:
        if not isinstance(keyBind, BizhawkKey):
            raise TypeError(f'keyBind argument is malformed: \"{keyBind}\"')
        elif not isinstance(action, CrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        bizhawkConnection = await self.__requireBizhawkConnection()

        try:
            # doing this is like we are pressing the key
            win32file.WriteFile(bizhawkConnection.connection, struct.pack('I', keyBind.intValue | 0x80000000))

            await asyncio.sleep(await self.__convertDelayFramesToSeconds())

            # doing this is like we are releasing the key
            win32file.WriteFile(bizhawkConnection.connection, struct.pack('I', keyBind.intValue))
        except Exception as e:
            self.__timber.log('BizhawkActionHandler', f'Encountered exception when attempting to send key press to Bizhawk ({keyBind=}) ({action=}) ({bizhawkConnection=}): {e}', e, traceback.format_exc())
            return CrowdControlActionHandleResult.ABANDON

        return CrowdControlActionHandleResult.OK

    async def handleButtonPressAction(
        self,
        action: ButtonPressCrowdControlAction
    ) -> CrowdControlActionHandleResult:
        if not isinstance(action, ButtonPressCrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        keyBind = await self.__bizhawkSettingsRepository.getButtonKeyBind(
            button = action.button
        )

        if keyBind is None:
            self.__timber.log('BizhawkActionHandler', f'No key bind is available for the given button press action ({action=}) ({keyBind=})')
            return CrowdControlActionHandleResult.ABANDON

        return await self.__handleBizhawkKeyPress(
            keyBind = keyBind,
            action = action
        )

    async def handleGameShuffleAction(
        self,
        action: GameShuffleCrowdControlAction
    ) -> CrowdControlActionHandleResult:
        if not isinstance(action, GameShuffleCrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        keyBind = await self.__bizhawkSettingsRepository.getGameShuffleKeyBind()

        if keyBind is None:
            self.__timber.log('BizhawkActionHandler', f'No key bind is available for the game shuffle action ({action=}) ({keyBind=})')
            return CrowdControlActionHandleResult.ABANDON

        return await self.__handleBizhawkKeyPress(
            keyBind = keyBind,
            action = action
        )

    async def __requireBizhawkConnection(self) -> BizhawkConnection:
        bizhawkConnection = self.__bizhawkConnection

        if bizhawkConnection is not None:
            return bizhawkConnection

        bizhawkProcessInfo = await self.__findBizhawkProcessInfo()

        if bizhawkProcessInfo is None:
            raise BizhawkProcessNotFoundException(f'Unable to find any Bizhawk process! ({bizhawkProcessInfo=})')

        # This is taken from this GitHub issue:
        # https://github.com/TASEmulators/BizHawk/issues/477#issuecomment-131264972
        pipeName = f'\\\\.\\pipe\\bizhawk-pid-{bizhawkProcessInfo.processId}-IPCKeyInput'

        try:
            connection = win32file.CreateFile(
                pipeName,
                win32file.GENERIC_WRITE,
                0, # No sharing
                None, # Default security attributes
                win32file.OPEN_EXISTING,
                0,
                None
            )
        except pywintypes.error as e:
            self.__timber.log('BizhawkActionHandler', f'Unable to connect to Bizhawk process ({bizhawkProcessInfo=}) ({pipeName=}): {e}', e, traceback.format_exc())
            raise BizhawkProcessCantBeConnectedTo(f'Unable to connect to Bizhawk process ({bizhawkProcessInfo=}) ({pipeName=}): {e}')

        bizhawkConnection = BizhawkActionHandler.BizhawkConnection(
            connection = connection,
            processId = bizhawkProcessInfo.processId,
            name = bizhawkProcessInfo.name
        )

        self.__bizhawkConnection = bizhawkConnection
        self.__lastBizhawkInputDateTime = datetime.now(self.__timeZoneRepository.getDefault())
        self.__timber.log('BizhawkActionHandler', f'Acquired Bizhawk connection ({bizhawkProcessInfo=})')

        return bizhawkConnection

    def start(self):
        if self.__isStarted:
            self.__timber.log('BizhawkActionHandler', 'Not starting BizhawkActionHandler as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('BizhawkActionHandler', 'Starting BizhawkActionHandler...')
        self.__backgroundTaskHelper.createTask(self.__startConnectionRefreshLoop())

    async def __startConnectionRefreshLoop(self):
        while True:
            await self.__closeConnectionIfUnused()
            await asyncio.sleep(self.__processConnectionCheckSleepTimeSeconds)
