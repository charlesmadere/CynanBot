from typing import Final

from .useChatterItemHelperInterface import UseChatterItemHelperInterface
from ..idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..machine.chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from ..mappers.itemRequestMessageParser import ItemRequestMessageParser
from ..models.useChatterItemAction import UseChatterItemAction
from ..models.useChatterItemRequest import UseChatterItemRequest
from ..models.useChatterItemResult import UseChatterItemResult
from ..settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...timber.timberInterface import TimberInterface


class UseChatterItemHelper(UseChatterItemHelperInterface):

    def __init__(
        self,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        chatterInventoryItemUseMachine: ChatterInventoryItemUseMachineInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        itemRequestMessageParser: ItemRequestMessageParser,
        timber: TimberInterface,
    ):
        if not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(chatterInventoryItemUseMachine, ChatterInventoryItemUseMachineInterface):
            raise TypeError(f'chatterInventoryItemUseMachine argument is malformed: \"{chatterInventoryItemUseMachine}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(itemRequestMessageParser, ItemRequestMessageParser):
            raise TypeError(f'itemRequestMessageParser argument is malformed: \"{itemRequestMessageParser}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__chatterInventoryItemUseMachine: Final[ChatterInventoryItemUseMachineInterface] = chatterInventoryItemUseMachine
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__itemRequestMessageParser: Final[ItemRequestMessageParser] = itemRequestMessageParser
        self.__timber: Final[TimberInterface] = timber

    async def useItem(self, request: UseChatterItemRequest) -> UseChatterItemResult:
        if not isinstance(request, UseChatterItemRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        if not await self.__chatterInventorySettings.isEnabled():
            return UseChatterItemResult.FEATURE_DISABLED

        itemType = request.itemType
        chatMessage = request.chatMessage

        if itemType is None:
            parseResult = await self.__itemRequestMessageParser.parse(
                chatMessage = request.chatMessage,
            )

            if parseResult is None:
                self.__timber.log('UseChatterItemHelper', f'Unable to parse the given item request ({parseResult=}) ({request=})')
                return UseChatterItemResult.INVALID_REQUEST

            itemType = parseResult.itemType
            chatMessage = parseResult.argument

        if itemType not in await self.__chatterInventorySettings.getEnabledItemTypes():
            return UseChatterItemResult.ITEM_DISABLED

        self.__chatterInventoryItemUseMachine.submitAction(UseChatterItemAction(
            ignoreInventory = request.ignoreInventory,
            itemType = itemType,
            actionId = await self.__chatterInventoryIdGenerator.generateActionId(),
            chatMessage = chatMessage,
            chatterUserId = request.chatterUserId,
            twitchChannelId = request.twitchChannelId,
            twitchChatMessageId = request.twitchChatMessageId,
            user = request.user,
        ))

        return UseChatterItemResult.OK
