import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from ..cheerActions.editCheerActionResult.alreadyDisabledEditCheerActionResult import \
    AlreadyDisabledEditCheerActionResult
from ..cheerActions.editCheerActionResult.notFoundEditCheerActionResult import NotFoundEditCheerActionResult
from ..cheerActions.editCheerActionResult.successfullyDisabledEditCheerActionResult import \
    SuccessfullyDisabledEditCheerActionResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class DisableCheerActionChatCommand(AbsChatCommand):

    @dataclass(frozen = True, slots = True)
    class Arguments:
        bits: int

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__cheerActionsRepository: Final[CheerActionsRepositoryInterface] = cheerActionsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!disablecheer(?:action)?\b', re.IGNORECASE),
        })

        self.__argumentsPattern: Final[Pattern] = re.compile(r'^\s*!\w+\s+(\d+)', re.IGNORECASE)

    @property
    def commandName(self) -> str:
        return 'DisableCheerActionChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.areCheerActionsEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        arguments = await self.__parseArguments(
            chatMessage = chatMessage,
        )

        if arguments is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Invalid arguments! Example use: !disablecheeraction 100',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Invalid arguments ({arguments=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        result = await self.__cheerActionsRepository.disableAction(
            bits = arguments.bits,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if isinstance(result, AlreadyDisabledEditCheerActionResult):
            self.__twitchChatMessenger.send(
                text = f'ⓘ Cheer action {arguments.bits} is already disabled: {result.cheerAction.printOut()}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        elif isinstance(result, NotFoundEditCheerActionResult):
            self.__twitchChatMessenger.send(
                text = f'⚠ Found no corresponding cheer action for bit amount {arguments.bits}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        elif isinstance(result, SuccessfullyDisabledEditCheerActionResult):
            self.__twitchChatMessenger.send(
                text = f'ⓘ Cheer action {arguments.bits} is now disabled: {result.cheerAction.printOut()}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        else:
            self.__timber.log(self.commandName, f'An unknown error occurred when trying to disable cheer action ({result=}) ({arguments=}) ({chatMessage=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ An unknown error occurred when trying to disable cheer action {arguments.bits}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Consumed ({result=}) ({arguments=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        return isStreamer or isAdministrator

    async def __parseArguments(self, chatMessage: TwitchChatMessage) -> Arguments | None:
        argumentsMatch = self.__argumentsPattern.match(chatMessage.text)
        if argumentsMatch is None:
            return None

        bitsString = argumentsMatch.group(1)

        try:
            bits = int(bitsString)
        except Exception as e:
            self.__timber.log(self.commandName, f'Failed to parse bitsString into an int ({bitsString=}) ({argumentsMatch=}) ({chatMessage=})', e, traceback.format_exc())
            return None

        if bits <= 0 or bits > utils.getIntMaxSafeSize():
            self.__timber.log(self.commandName, f'The bits value is out of bounds ({bits=}) ({bitsString=}) ({argumentsMatch=}) ({chatMessage=})')
            return None

        return DisableCheerActionChatCommand.Arguments(
            bits = bits,
        )

