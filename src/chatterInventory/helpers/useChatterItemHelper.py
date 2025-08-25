from typing import Final

from .useChatterItemHelperInterface import UseChatterItemHelperInterface
from ..machine.chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from ..mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..models.useChatterItemRequest import UseChatterItemRequest
from ..models.useChatterItemResult import UseChatterItemResult
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface


class UseChatterItemHelper(UseChatterItemHelperInterface):

    def __init__(
        self,
        chatterInventoryItemUseMachine: ChatterInventoryItemUseMachineInterface,
        chatterInventoryMapper: ChatterInventoryMapperInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface,
    ):
        if not isinstance(chatterInventoryItemUseMachine, ChatterInventoryItemUseMachineInterface):
            raise TypeError(f'chatterInventoryItemUseMachine argument is malformed: \"{chatterInventoryItemUseMachine}\"')
        elif not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')

        self.__chatterInventoryItemUseMachine: Final[ChatterInventoryItemUseMachineInterface] = chatterInventoryItemUseMachine
        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine

    async def useItem(self, request: UseChatterItemRequest) -> UseChatterItemResult:
        if not isinstance(request, UseChatterItemRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        if not await self.__chatterInventorySettings.isEnabled():
            return UseChatterItemResult.FEATURE_DISABLED

        itemType = request.itemType
        chatMessage = request.chatMessage

        if itemType is None:
            messageSplits = utils.getCleanedSplits(chatMessage)

            if len(messageSplits) == 0:
                self.__timber.log('UseChatterItemHelper', f'The given request has no itemType or chatMessage to work with ({messageSplits=}) ({request=})')
                return UseChatterItemResult.INVALID_REQUEST

            itemType = await self.__chatterInventoryMapper.parseItemType(
                itemType = messageSplits[0],
            )

            if itemType is None:
                self.__timber.log('UseChatterItemHelper', f'Unable to parse valid ChatterItemType from the given chatMessage ({itemType=}) ({messageSplits=}) ({request=})')
                return UseChatterItemResult.INVALID_REQUEST

            chatMessage = ' '.join(messageSplits[1:])

        # TODO
        raise RuntimeError()
