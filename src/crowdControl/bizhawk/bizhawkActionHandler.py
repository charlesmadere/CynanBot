import traceback
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

import psutil

from .bizhawkKey import BizhawkKey
from .bizhawkSettingsRepositoryInterface import BizhawkSettingsRepositoryInterface
from .exceptions import BizhawkProcessNotFoundException
from ..actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ..actions.crowdControlAction import CrowdControlAction
from ..actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..crowdControlActionHandleResult import CrowdControlActionHandleResult
from ..crowdControlActionHandler import CrowdControlActionHandler
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class BizhawkActionHandler(CrowdControlActionHandler):

    @dataclass(frozen = True)
    class BizhawkProcess:
        foundDateTime: datetime
        processId: int
        name: str

    @dataclass(frozen = True)
    class GenericProcess:
        processId: int
        name: str

    def __init__(
        self,
        bizhawkSettingsRepository: BizhawkSettingsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        keyPressDelayMillis: int = 64,
        processCacheTimeToLive: timedelta = timedelta(minutes = 15)
    ):
        if not isinstance(bizhawkSettingsRepository, BizhawkSettingsRepositoryInterface):
            raise TypeError(f'bizhawkSettingsRepository argument is malformed: \"{bizhawkSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidInt(keyPressDelayMillis):
            raise TypeError(f'keyPressDelayMillis argument is malformed: \"{keyPressDelayMillis}\"')
        elif keyPressDelayMillis < 32 or keyPressDelayMillis > 250:
            raise ValueError(f'keyPressDelayMillis argument is out of bounds: {keyPressDelayMillis}')
        elif not isinstance(processCacheTimeToLive, timedelta):
            raise TypeError(f'processCacheTimeToLive argument is malformed: \"{processCacheTimeToLive}\"')

        self.__bizhawkSettingsRepository: BizhawkSettingsRepositoryInterface = bizhawkSettingsRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__keyPressDelayMillis: int = keyPressDelayMillis
        self.__processCacheTimeToLive: timedelta = processCacheTimeToLive

        self.__bizhawkProcess: BizhawkActionHandler.BizhawkProcess | None = None

    async def __handleBizhawkKeyPress(
        self,
        keyBind: BizhawkKey,
        action: CrowdControlAction
    ) -> CrowdControlActionHandleResult:
        if not isinstance(keyBind, BizhawkKey):
            raise TypeError(f'keyBind argument is malformed: \"{keyBind}\"')
        elif not isinstance(action, CrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        bizhawkProcess = await self.__requireBizhawkProcess()

        # This is taken from this GitHub issue:
        # https://github.com/TASEmulators/BizHawk/issues/477#issuecomment-131264972
        pipeName = f'bizhawk-pid-{bizhawkProcess.processId}-IPCKeyInput'

        # TODO
        return CrowdControlActionHandleResult.ABANDON

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
            return CrowdControlActionHandleResult.ABANDON
        else:
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
            return CrowdControlActionHandleResult.ABANDON
        else:
            return await self.__handleBizhawkKeyPress(
                keyBind = keyBind,
                action = action
            )

    async def __requireBizhawkProcess(self) -> BizhawkProcess:
        bizhawkProcess = self.__bizhawkProcess

        if bizhawkProcess is not None:
            now = datetime.now(self.__timeZoneRepository.getDefault())

            if bizhawkProcess.foundDateTime + self.__processCacheTimeToLive >= now:
                return bizhawkProcess
            else:
                bizhawkProcess = None

        bizhawkProcessName = await self.__bizhawkSettingsRepository.getProcessName()
        allProcesses: list[BizhawkActionHandler.GenericProcess] = list()

        try:
            for proc in psutil.process_iter(['name', 'pid']):
                processId: int | Any | None = proc.info.get('pid', None)
                processName: str | Any | None = proc.info.get('name', None)

                if not utils.isValidInt(processId) or not utils.isValidStr(processName):
                    continue

                allProcesses.append(BizhawkActionHandler.GenericProcess(
                    processId = processId,
                    name = processName
                ))

                if bizhawkProcessName not in processName:
                    continue
                elif bizhawkProcess is None:
                    now = datetime.now(self.__timeZoneRepository.getDefault())

                    bizhawkProcess = BizhawkActionHandler.BizhawkProcess(
                        foundDateTime = now,
                        processId = processId,
                        name = processName
                    )
                else:
                    self.__timber.log('BizhawkActionHandler', f'More than one BizHawk process was found! ({bizhawkProcess=}) ({bizhawkProcessName=}) ({proc=}) ({allProcesses=})')
        except Exception as e:
            self.__timber.log('BizhawkActionHandler', f'Encountered exception when looping through available processes ({bizhawkProcess=}) ({bizhawkProcessName=}) ({allProcesses=}): {e}', e, traceback.format_exc())

        if bizhawkProcess is None:
            raise BizhawkProcessNotFoundException(f'Unable to find any Bizhawk process! ({bizhawkProcess=}) ({bizhawkProcessName=}) ({allProcesses=})')

        self.__bizhawkProcess = bizhawkProcess
        return bizhawkProcess
