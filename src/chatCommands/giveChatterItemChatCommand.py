import random
import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ..chatterInventory.machine.chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from ..chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..chatterInventory.models.chatterItemType import ChatterItemType
from ..chatterInventory.models.tradeChatterItemAction import TradeChatterItemAction
from ..chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class GiveChatterItemChatCommand(AbsChatCommand2):

    @dataclass(frozen = True, slots = True)
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

        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__chatterInventoryItemUseMachine: Final[ChatterInventoryItemUseMachineInterface] = chatterInventoryItemUseMachine
        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!give(?:chatter)?item\b', re.IGNORECASE),
            re.compile(r'^\s*!itemgive\b', re.IGNORECASE),
        })

    async def __chooseRandomEnabledItemType(self) -> str:
        enabledItemTypes = await self.__chatterInventorySettings.getEnabledItemTypes()
        randomItemType = random.choice(list(enabledItemTypes))
        return await self.__chatterInventoryMapper.serializeItemType(randomItemType)

    @property
    def commandName(self) -> str:
        return 'GiveChatterItemChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterInventoryEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__chatterInventorySettings.isEnabled():
            return ChatCommandResult.IGNORED

        arguments = await self.__parseArguments(chatMessage)

        if arguments is None:
            randomItemType = await self.__chooseRandomEnabledItemType()

            self.__twitchChatMessenger.send(
                text = f'⚠ Invalid arguments! Example use: !give @{chatMessage.chatterUserName} {randomItemType}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            return ChatCommandResult.HANDLED

        elif chatMessage.chatterUserId == arguments.chatterUserId:
            randomItemType = await self.__chooseRandomEnabledItemType()

            self.__twitchChatMessenger.send(
                text = f'⚠ You can\'t give yourself an item! Example use: !give @{chatMessage.chatterUserName} {randomItemType}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            return ChatCommandResult.HANDLED

        actionId = await self.__chatterInventoryIdGenerator.generateActionId()

        self.__chatterInventoryItemUseMachine.submitAction(TradeChatterItemAction(
            itemType = arguments.itemType,
            tradeAmount = arguments.giveAmount,
            actionId = actionId,
            fromChatterUserId = chatMessage.chatterUserId,
            toChatterUserId = arguments.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = chatMessage.twitchChatMessageId,
            user = chatMessage.twitchUser,
        ))

        self.__timber.log(self.commandName, f'Handled ({actionId=}) ({arguments=}) ({chatMessage=})')
        return ChatCommandResult.HANDLED

    async def __parseArguments(self, chatMessage: TwitchChatMessage) -> Arguments | None:
        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 3:
            return None

        chatterUserName: str | None = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(chatterUserName) or not utils.strContainsAlphanumericCharacters(chatterUserName):
            return None

        chatterUserId = await self.__userIdsRepository.fetchUserId(
            userName = chatterUserName,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = chatMessage.twitchChannelId,
            ),
        )

        if not utils.isValidStr(chatterUserId):
            self.__timber.log(self.commandName, f'Failed to fetch user ID for the given chatter username ({chatterUserId=}) ({chatterUserName=}) ({splits=}) ({chatMessage=})')
            return None

        itemTypeString: str | None = splits[2]

        itemType = await self.__chatterInventoryMapper.parseItemType(
            itemType = itemTypeString,
        )

        if itemType is None:
            self.__timber.log(self.commandName, f'Failed to parse itemTypeString into a ChatterItemType ({itemType=}) ({itemTypeString=}) ({splits=}) ({chatMessage=})')
            return None

        giveAmount = 1

        if len(splits) >= 4:
            giveAmountString: str | None = splits[3]

            try:
                giveAmount = int(giveAmountString)
            except Exception as e:
                self.__timber.log(self.commandName, f'Failed to parse giveAmountString into an int ({giveAmountString=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())
                return None

            if giveAmount < 1 or giveAmount > utils.getShortMaxSafeSize():
                self.__timber.log(self.commandName, f'The giveAmount value is out of bounds ({giveAmount=}) ({giveAmountString=}) ({splits=}) ({chatMessage})')
                return None

        return GiveChatterItemChatCommand.Arguments(
            itemType = itemType,
            giveAmount = giveAmount,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
        )
