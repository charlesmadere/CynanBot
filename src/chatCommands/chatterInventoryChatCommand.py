import locale
from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ..chatterInventory.models.chatterItemType import ChatterItemType
from ..chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class ChatterInventoryChatCommand(AbsChatCommand):

    def __init__(
        self,
        chatterInventoryHelper: ChatterInventoryHelperInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__chatterInventoryHelper: Final[ChatterInventoryHelperInterface] = chatterInventoryHelper
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isChatterInventoryEnabled:
            return

        inventory = await self.__chatterInventoryHelper.get(
            chatterUserId = ctx.getAuthorId(),
            twitchChannelId = await ctx.getTwitchChannelId(),
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

        await self.__twitchChatMessenger.send(
            text = f'ⓘ Your inventory: {inventoryString}',
            twitchChannelId = await ctx.getTwitchChannelId(),
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('ChatterInventoryChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
