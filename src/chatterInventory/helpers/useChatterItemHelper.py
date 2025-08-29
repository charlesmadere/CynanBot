from typing import Final

from .useChatterItemHelperInterface import UseChatterItemHelperInterface
from ..idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..machine.chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from ..mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..models.useChatterItemAction import UseChatterItemAction
from ..models.useChatterItemRequest import UseChatterItemRequest
from ..models.useChatterItemResult import UseChatterItemResult
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class UseChatterItemHelper(UseChatterItemHelperInterface):

    def __init__(
        self,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        chatterInventoryItemUseMachine: ChatterInventoryItemUseMachineInterface,
        chatterInventoryMapper: ChatterInventoryMapperInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
    ):
        if not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(chatterInventoryItemUseMachine, ChatterInventoryItemUseMachineInterface):
            raise TypeError(f'chatterInventoryItemUseMachine argument is malformed: \"{chatterInventoryItemUseMachine}\"')
        elif not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__chatterInventoryItemUseMachine: Final[ChatterInventoryItemUseMachineInterface] = chatterInventoryItemUseMachine
        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber

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

        if itemType not in await self.__chatterInventorySettings.getEnabledItemTypes():
            return UseChatterItemResult.ITEM_DISABLED

        self.__chatterInventoryItemUseMachine.submitAction(UseChatterItemAction(
            ignoreInventory = request.ignoreInventory,
            itemType = itemType,
            pointRedemption = request.pointRedemption,
            actionId = await self.__chatterInventoryIdGenerator.generateActionId(),
            chatMessage = chatMessage,
            chatterUserId = request.chatterUserId,
            twitchChannelId = request.twitchChannelId,
            twitchChatMessageId = request.twitchChatMessageId,
            user = request.user,
        ))

        return UseChatterItemResult.OK
