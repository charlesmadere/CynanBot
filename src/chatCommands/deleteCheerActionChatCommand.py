import traceback
from typing import Final

from .absChatCommand import AbsChatCommand
from ..cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class DeleteCheerActionChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
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
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__cheerActionsRepository: Final[CheerActionsRepositoryInterface] = cheerActionsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.areCheerActionsEnabled:
            return

        userId = await self.__userIdsRepository.requireUserId(user.handle)
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('DeleteCheerActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2 or not utils.strContainsAlphanumericCharacters(splits[1]):
            self.__timber.log('DeleteCheerActionCommand', f'Incorrect arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
            self.__twitchChatMessenger.send(
                text = f'⚠ Bit amount is necessary for the !deletecheeraction command. Example: !deletecheeraction 100',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        try:
            bits = int(splits[1])
        except Exception as e:
            self.__timber.log('DeleteCheerActionCommand', f'Cheer action was attempted to be deleted by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but was unable to convert: {e}', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Bit amount is necessary for the !deletecheeraction command. Example: !deletecheeraction 100',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        action = await self.__cheerActionsRepository.deleteAction(
            bits = bits,
            twitchChannelId = userId,
        )

        if action is None:
            self.__timber.log('DeleteCheerActionCommand', f'Cheer {bits} was attempted to be deleted by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no corresponding cheer action was found')
            self.__twitchChatMessenger.send(
                text = f'⚠ Could not find any corresponding cheer action with bits \"{bits}\"',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        else:
            self.__twitchChatMessenger.send(
                text = f'ⓘ Deleted cheer action — {action}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('DeleteCheerActionCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
