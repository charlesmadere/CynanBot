import locale
import random
import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from ..chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..chatterInventory.models.chatterItemType import ChatterItemType
from ..chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitch.userIds.twitchUserIdsHelperInterface import TwitchUserIdsHelperInterface


class FreeGiveChatterItemChatCommand(AbsChatCommand):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        itemType: ChatterItemType
        giveAmount: int
        chatterUserId: str
        chatterUserLogin: str
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
        twitchUserIdsHelper: TwitchUserIdsHelperInterface,
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
        elif not isinstance(twitchUserIdsHelper, TwitchUserIdsHelperInterface):
            raise TypeError(f'twitchUserIdsHelper argument is malformed: \"{twitchUserIdsHelper}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__chatterInventoryHelper: Final[ChatterInventoryHelperInterface] = chatterInventoryHelper
        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChannelEditorsRepository: Final[TwitchChannelEditorsRepositoryInterface] = twitchChannelEditorsRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUserIdsHelper: Final[TwitchUserIdsHelperInterface] = twitchUserIdsHelper

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!free(?:give)?(?:chatter)?item\b', re.IGNORECASE),
            re.compile(r'^\s*!free(?:chatter)?item(?:give)?\b', re.IGNORECASE),
            re.compile(r'^\s*!givefree(?:chatter)?item\b', re.IGNORECASE),
        })

        self.__argumentsPattern: Final[Pattern] = re.compile(r'^\s*!\w+\s+@?(\w+)\s+(\w+)(?:\s+(-?\d+))?', re.IGNORECASE)

    async def __chooseRandomEnabledItemType(self) -> str:
        enabledItemTypes = await self.__chatterInventorySettings.getEnabledItemTypes()
        randomItemType = random.choice(list(enabledItemTypes))
        return await self.__chatterInventoryMapper.serializeItemType(randomItemType)

    @property
    def commandName(self) -> str:
        return 'FreeGiveChatterItemChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterInventoryEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__chatterInventorySettings.isEnabled():
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        arguments = await self.__parseArguments(
            chatMessage = chatMessage,
        )

        if arguments is None:
            randomItemType = await self.__chooseRandomEnabledItemType()

            self.__twitchChatMessenger.send(
                text = f'⚠ Invalid arguments! Example use: !freegive @{chatMessage.chatterUserName} {randomItemType}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Invalid arguments ({arguments=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        updatedInventory = await self.__chatterInventoryHelper.give(
            itemType = arguments.itemType,
            giveAmount = arguments.giveAmount,
            chatterUserId = arguments.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        inventoryStrings: list[str] = list()

        for itemType in ChatterItemType:
            if itemType not in await self.__chatterInventorySettings.getEnabledItemTypes():
                continue

            amount = updatedInventory[itemType]
            amountString = locale.format_string("%d", amount, grouping = True)

            match amount:
                case 0: continue
                case 1: inventoryStrings.append(f'{amountString} {itemType.humanName}')
                case _: inventoryStrings.append(f'{amountString} {itemType.pluralHumanName}')

        inventoryString: str

        if len(inventoryStrings) == 0:
            inventoryString = f'inventory is empty {utils.getRandomSadEmoji()}'
        else:
            inventoryString = ', '.join(inventoryStrings)

        self.__twitchChatMessenger.send(
            text = f'ⓘ Updated inventory for @{updatedInventory.chatterUserData.getUserLogin()} — {inventoryString}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Consumed ({updatedInventory=}) ({arguments=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        isEditor = await self.__twitchChannelEditorsRepository.isEditor(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        return isStreamer or isAdministrator or isEditor

    async def __parseArguments(self, chatMessage: TwitchChatMessage) -> Arguments | None:
        argumentsMatch = self.__argumentsPattern.match(chatMessage.text)
        if argumentsMatch is None:
            return None

        chatterUserName = argumentsMatch.group(1)

        try:
            chatterUserData = await self.__twitchUserIdsHelper.requireByLoginOrName(
                userLoginOrName = chatterUserName,
                twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                    twitchChannelId = chatMessage.twitchChannelId,
                ),
            )
        except Exception as e:
            self.__timber.log(self.commandName, f'Failed to fetch user ID for the given chatter username ({chatterUserName=}) ({argumentsMatch=}) ({chatMessage=})', e, traceback.format_exc())
            return None

        itemTypeString = argumentsMatch.group(2)

        try:
            itemType = await self.__chatterInventoryMapper.requireItemType(
                itemType = itemTypeString,
            )
        except Exception as e:
            self.__timber.log(self.commandName, f'Failed to parse itemTypeString into a ChatterItemType ({itemTypeString=}) ({chatterUserData=}) ({chatterUserName=}) ({argumentsMatch=}) ({chatMessage=})', e, traceback.format_exc())
            return None

        giveAmount = 1
        giveAmountString = argumentsMatch.group(3)

        if utils.isValidStr(giveAmountString):
            try:
                giveAmount = int(giveAmountString)
            except Exception as e:
                self.__timber.log(self.commandName, f'Failed to parse giveAmountString into an int ({giveAmountString=}) ({itemTypeString=}) ({chatterUserData=}) ({chatterUserName=}) ({argumentsMatch=}) ({chatMessage=})', e, traceback.format_exc())
                return None

            if giveAmount < utils.getShortMinSafeSize() or giveAmount > utils.getShortMaxSafeSize():
                self.__timber.log(self.commandName, f'The giveAmount value is out of bounds ({giveAmount=}) ({giveAmountString=}) ({itemTypeString=}) ({chatterUserData=}) ({chatterUserName=}) ({argumentsMatch=}) ({chatMessage=})')
                return None

        return FreeGiveChatterItemChatCommand.Arguments(
            itemType = itemType,
            giveAmount = giveAmount,
            chatterUserId = chatterUserData.userId,
            chatterUserLogin = chatterUserData.userLogin,
            chatterUserName = chatterUserData.userName,
        )
