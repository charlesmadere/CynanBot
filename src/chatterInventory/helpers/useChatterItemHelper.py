from typing import Final

from .useChatterItemHelperInterface import UseChatterItemHelperInterface
from ..models.useChatterItemRequest import UseChatterItemRequest
from ..models.useChatterItemResult import UseChatterItemResult
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...timber.timberInterface import TimberInterface
from ...timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface


class UseChatterItemHelper(UseChatterItemHelperInterface):

    def __init__(
        self,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface,
    ):
        if not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')

        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine

    async def useItem(self, request: UseChatterItemRequest) -> UseChatterItemResult:
        if not isinstance(request, UseChatterItemRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        if not await self.__chatterInventorySettings.isEnabled():
            return UseChatterItemResult.FEATURE_DISABLED

        # TODO
        raise RuntimeError()
