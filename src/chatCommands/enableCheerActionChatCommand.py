import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from ..cheerActions.editCheerActionResult.alreadyEnabledEditCheerActionResult import AlreadyEnabledEditCheerActionResult
from ..cheerActions.editCheerActionResult.notFoundEditCheerActionResult import NotFoundEditCheerActionResult
from ..cheerActions.editCheerActionResult.successfullyEnabledEditCheerActionResult import \
    SuccessfullyEnabledEditCheerActionResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class EnableCheerActionChatCommand(AbsChatCommand):

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
            re.compile(r'^\s*!enablecheeraction\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'EnableCheerActionChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.areCheerActionsEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__twitchChatMessenger.send(
                text = f'⚠ Bits amount argument is necessary for the !enablecheeraction command. Example: !enablecheeraction 100',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.CONSUMED

        bitsString = splits[1]

        try:
            bits = int(bitsString)
        except Exception as e:
            self.__timber.log(self.commandName, f'Bits amount is malformed ({bitsString=}) ({chatMessage=})', e, traceback.format_exc())

            self.__twitchChatMessenger.send(
                text = f'⚠ Bits amount argument is malformed. Example: !enablecheeraction 100',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.CONSUMED

        if bits < 1 or bits > utils.getIntMaxSafeSize():
            self.__timber.log(self.commandName, f'Bits amount is out of bounds ({bits=}) ({bitsString=}) ({chatMessage=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ Bits amount argument is out of bounds. Example: !enablecheeraction 100',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.CONSUMED

        result = await self.__cheerActionsRepository.enableAction(
            bits = bits,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if isinstance(result, AlreadyEnabledEditCheerActionResult):
            self.__twitchChatMessenger.send(
                text = f'ⓘ Cheer action {bits} is already enabled: {result.cheerAction.printOut()}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        elif isinstance(result, NotFoundEditCheerActionResult):
            self.__twitchChatMessenger.send(
                text = f'⚠ Found no corresponding cheer action for bit amount {bits}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        elif isinstance(result, SuccessfullyEnabledEditCheerActionResult):
            self.__twitchChatMessenger.send(
                text = f'ⓘ Cheer action {bits} is now enabled: {result.cheerAction.printOut()}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        else:
            self.__timber.log(self.commandName, f'An unknown error occurred when trying to enable cheer action ({result=}) ({bits=}) ({chatMessage=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ An unknown error occurred when trying to enable cheer action {bits}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Handled ({result=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId
        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()
        return isStreamer or isAdministrator
