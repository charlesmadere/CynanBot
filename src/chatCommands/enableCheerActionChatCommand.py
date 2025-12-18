import traceback
from typing import Final

from .absChatCommand import AbsChatCommand
from ..cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from ..cheerActions.editCheerActionResult.alreadyEnabledEditCheerActionResult import AlreadyEnabledEditCheerActionResult
from ..cheerActions.editCheerActionResult.notFoundEditCheerActionResult import NotFoundEditCheerActionResult
from ..cheerActions.editCheerActionResult.successfullyEnabledEditCheerActionResult import \
    SuccessfullyEnabledEditCheerActionResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class EnableCheerActionChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__cheerActionsRepository: Final[CheerActionsRepositoryInterface] = cheerActionsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('EnableCheerActionChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__twitchChatMessenger.send(
                text = f'⚠ Bits amount argument is necessary for the !enablecheeraction command. Example: !enablecheeraction 100',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        bitsString: str | None = splits[1]

        try:
            bits = int(bitsString)
        except Exception as e:
            self.__timber.log('EnableCheerActionChatCommand', f'Bits amount given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} is malformed ({bitsString=}): {e}', e, traceback.format_exc())

            self.__twitchChatMessenger.send(
                text = f'⚠ Bits amount argument is malformed. Example: !enablecheeraction 100',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId()
            )
            return

        if bits < 1 or bits > utils.getIntMaxSafeSize():
            self.__timber.log('EnableCheerActionChatCommand', f'Bits amount given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} is out of bounds ({bitsString=} ({bits=})')

            self.__twitchChatMessenger.send(
                text = f'⚠ Bits amount argument is out of bounds. Example: !enablecheeraction 100',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        result = await self.__cheerActionsRepository.enableAction(
            bits = bits,
            twitchChannelId = userId,
        )

        if isinstance(result, AlreadyEnabledEditCheerActionResult):
            self.__twitchChatMessenger.send(
                text = f'ⓘ Cheer action {bits} is already enabled: {result.cheerAction.printOut()}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        elif isinstance(result, NotFoundEditCheerActionResult):
            self.__twitchChatMessenger.send(
                text = f'⚠ Found no corresponding cheer action for bit amount {bits}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        elif isinstance(result, SuccessfullyEnabledEditCheerActionResult):
            self.__twitchChatMessenger.send(
                text = f'ⓘ Cheer action {bits} is now enabled: {result.cheerAction.printOut()}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        else:
            self.__timber.log('EnableCheerActionChatCommand', f'An unknown error occurred when {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried to enable cheer action {bits}')

            self.__twitchChatMessenger.send(
                text = f'⚠ An unknown error occurred when trying to enable cheer action {bits}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('EnableCheerActionChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
