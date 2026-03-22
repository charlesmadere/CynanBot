import locale
import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ..chatterInventory.models.chatterItemType import ChatterItemType
from ..chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class ChatterInventoryChatCommand(AbsChatCommand2):

    def __init__(
        self,
        chatterInventoryHelper: ChatterInventoryHelperInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__chatterInventoryHelper: Final[ChatterInventoryHelperInterface] = chatterInventoryHelper
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!(?:my)?(?:inv)?entory\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'ChatterInventoryChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterInventoryEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__chatterInventorySettings.isEnabled():
            return ChatCommandResult.IGNORED

        inventory = await self.__chatterInventoryHelper.get(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        inventoryStrings: list[str] = list()

        for itemType in ChatterItemType:
            if itemType not in await self.__chatterInventorySettings.getEnabledItemTypes():
                continue

            amount = inventory[itemType]
            amountString = locale.format_string("%d", amount, grouping = True)

            if amount == 1:
                inventoryStrings.append(f'{amountString} {itemType.humanName}')
            else:
                inventoryStrings.append(f'{amountString} {itemType.pluralHumanName}')

        inventoryString = ', '.join(inventoryStrings)

        self.__twitchChatMessenger.send(
            text = f'ⓘ Your inventory: {inventoryString}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log('ChatterInventoryChatCommand', f'Handled ({inventory=})')
        return ChatCommandResult.HANDLED
