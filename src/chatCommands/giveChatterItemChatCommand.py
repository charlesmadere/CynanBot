import random
import traceback
from dataclasses import dataclass
from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..chatterInventory.machine.chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from ..chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..chatterInventory.models.chatterItemType import ChatterItemType
from ..chatterInventory.models.tradeChatterItemAction import TradeChatterItemAction
from ..chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class GiveChatterItemChatCommand(AbsChatCommand):

    @dataclass(frozen = True)
    class Arguments:
        itemType: ChatterItemType
        giveAmount: int
        chatterUserId: str
        chatterUserName: str

    def __init__(
        self,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        chatterInventoryItemUseMachine: ChatterInventoryItemUseMachineInterface,
        chatterInventoryMapper: ChatterInventoryMapperInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
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
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__chatterInventoryItemUseMachine: Final[ChatterInventoryItemUseMachineInterface] = chatterInventoryItemUseMachine
        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
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

        arguments = await self.__parseArguments(
            messageContent = ctx.getMessageContent(),
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        if arguments is None:
            randomItemType = await self.__chooseRandomEnabledItemType()

            self.__twitchChatMessenger.send(
                text = f'⚠ Invalid arguments! Example use: !give @{ctx.getAuthorName()} {randomItemType}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return
        elif ctx.getAuthorId() == arguments.chatterUserId:
            randomItemType = await self.__chooseRandomEnabledItemType()

            self.__twitchChatMessenger.send(
                text = f'⚠ You can\'t give yourself an item! Example use: !give @{ctx.getAuthorName()} {randomItemType}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        self.__chatterInventoryItemUseMachine.submitAction(TradeChatterItemAction(
            itemType = arguments.itemType,
            tradeAmount = arguments.giveAmount,
            actionId = await self.__chatterInventoryIdGenerator.generateActionId(),
            fromChatterUserId = ctx.getAuthorId(),
            toChatterUserId = arguments.chatterUserId,
            twitchChannelId = await ctx.getTwitchChannelId(),
            twitchChatMessageId = await ctx.getMessageId(),
            user = user,
        ))

        self.__timber.log('GiveChatterItemChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

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
        except:
            self.__timber.log('GiveChatterItemChatCommand', f'Failed to fetch user ID for the given chatter username ({chatterUserName=}) ({splits=})')
            return None

        itemTypeString = splits[2]

        itemType = await self.__chatterInventoryMapper.parseItemType(
            itemType = itemTypeString,
        )

        if itemType is None:
            self.__timber.log('GiveChatterItemChatCommand', f'Failed to parse itemTypeString into a ChatterItemType ({itemTypeString=}) ({splits=})')
            return None

        giveAmount = 1

        if len(splits) >= 4:
            giveAmountString = splits[3]

            try:
                giveAmount = int(giveAmountString)
            except Exception as e:
                self.__timber.log('GiveChatterItemChatCommand', f'Failed to parse giveAmountString into an int ({giveAmountString=}) ({splits=})', e, traceback.format_exc())
                return None

            if giveAmount < 1 or giveAmount > utils.getShortMaxSafeSize():
                self.__timber.log('GiveChatterItemChatCommand', f'The giveAmount value is out of bounds ({giveAmount=}) ({giveAmountString=}) ({splits=})')
                return None

        return GiveChatterItemChatCommand.Arguments(
            itemType = itemType,
            giveAmount = giveAmount,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
        )
