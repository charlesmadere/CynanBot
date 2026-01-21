import locale
import random
import traceback
from dataclasses import dataclass
from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ..chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..chatterInventory.models.chatterItemType import ChatterItemType
from ..chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class FreeGiveChatterItemChatCommand(AbsChatCommand):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        itemType: ChatterItemType
        giveAmount: int
        chatterUserId: str
        chatterUserName: str

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        chatterInventoryHelper: ChatterInventoryHelperInterface,
        chatterInventoryMapper: ChatterInventoryMapperInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelEditorsRepository, TwitchChannelEditorsRepositoryInterface):
            raise TypeError(f'twitchChannelEditorsRepository argument is malformed: \"{twitchChannelEditorsRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__chatterInventoryHelper: Final[ChatterInventoryHelperInterface] = chatterInventoryHelper
        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChannelEditorsRepository: Final[TwitchChannelEditorsRepositoryInterface] = twitchChannelEditorsRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def __chooseRandomEnabledItemType(self) -> str:
        enabledItemTypes = await self.__chatterInventorySettings.getEnabledItemTypes()
        randomItemType = random.choice(list(enabledItemTypes))
        return await self.__chatterInventoryMapper.serializeItemType(randomItemType)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isChatterInventoryEnabled:
            return
        elif not await self.__chatterInventorySettings.isEnabled():
            return

        twitchChannelId = await ctx.getTwitchChannelId()
        editorIds = await self.__twitchChannelEditorsRepository.fetchEditorIds(twitchChannelId)
        administratorId = await self.__administratorProvider.getAdministratorUserId()

        if ctx.getAuthorId() != twitchChannelId and ctx.getAuthorId() != administratorId and ctx.getAuthorId() not in editorIds:
            self.__timber.log('FreeGiveChatterItemChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        arguments = await self.__parseArguments(
            messageContent = ctx.getMessageContent(),
            twitchChannelId = twitchChannelId,
        )

        if arguments is None:
            randomItemType = await self.__chooseRandomEnabledItemType()

            self.__twitchChatMessenger.send(
                text = f'⚠ Invalid arguments! Example use: !freegive @{ctx.getAuthorName()} {randomItemType}',
                twitchChannelId = twitchChannelId,
                replyMessageId = await ctx.getMessageId(),
            )
            return

        updatedInventory = await self.__chatterInventoryHelper.give(
            itemType = arguments.itemType,
            giveAmount = arguments.giveAmount,
            chatterUserId = arguments.chatterUserId,
            twitchChannelId = twitchChannelId,
        )

        inventoryStrings: list[str] = list()

        for itemType in ChatterItemType:
            if itemType not in await self.__chatterInventorySettings.getEnabledItemTypes():
                continue

            amount = updatedInventory[itemType]
            amountString = locale.format_string("%d", amount, grouping = True)

            if amount == 1:
                inventoryStrings.append(f'{amountString} {itemType.humanName}')
            else:
                inventoryStrings.append(f'{amountString} {itemType.pluralHumanName}')

        inventoryString = ', '.join(inventoryStrings)

        self.__twitchChatMessenger.send(
            text = f'ⓘ Updated inventory for @{updatedInventory.chatterUserName} — {inventoryString}',
            twitchChannelId = twitchChannelId,
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('FreeGiveChatterItemChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

    async def __parseArguments(
        self,
        messageContent: str | None,
        twitchChannelId: str,
    ) -> Arguments | None:
        if not utils.isValidStr(messageContent):
            return None

        splits = utils.getCleanedSplits(messageContent)
        if len(splits) < 3:
            return None

        chatterUserName = utils.removePreceedingAt(splits[1])

        try:
            chatterUserId = await self.__userIdsRepository.requireUserId(
                userName = chatterUserName,
                twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                    twitchChannelId = twitchChannelId,
                ),
            )
        except Exception as e:
            self.__timber.log('FreeGiveChatterItemChatCommand', f'Failed to fetch user ID for the given chatter username ({chatterUserName=}) ({splits=})', e, traceback.format_exc())
            return None

        itemTypeString = splits[2]
        itemType = await self.__chatterInventoryMapper.parseItemType(itemTypeString)

        if itemType is None:
            self.__timber.log('FreeGiveChatterItemChatCommand', f'Failed to parse itemTypeString into a ChatterItemType ({itemTypeString=}) ({splits=})')
            return None

        giveAmount = 1

        if len(splits) >= 4:
            giveAmountString = splits[3]

            try:
                giveAmount = int(giveAmountString)
            except Exception as e:
                self.__timber.log('FreeGiveChatterItemChatCommand', f'Failed to parse giveAmountString into an int ({giveAmountString=}) ({splits=})', e, traceback.format_exc())
                return None

            if giveAmount < utils.getShortMinSafeSize() or giveAmount > utils.getShortMaxSafeSize():
                self.__timber.log('FreeGiveChatterItemChatCommand', f'The giveAmount value is out of bounds ({giveAmount=}) ({giveAmountString=}) ({splits=})')
                return None

        return FreeGiveChatterItemChatCommand.Arguments(
            itemType = itemType,
            giveAmount = giveAmount,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
        )
