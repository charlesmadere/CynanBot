from typing import Final

from .absChatCommand import AbsChatCommand
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..recurringActions.recurringActionsHelperInterface import RecurringActionsHelperInterface
from ..recurringActions.recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class RemoveRecurringWeatherActionCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        recurringActionsHelper: RecurringActionsHelperInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(recurringActionsHelper, RecurringActionsHelperInterface):
            raise TypeError(f'recurringActionsHelper argument is malformed: \"{recurringActionsHelper}\"')
        elif not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__recurringActionsHelper: Final[RecurringActionsHelperInterface] = recurringActionsHelper
        self.__recurringActionsRepository: Final[RecurringActionsRepositoryInterface] = recurringActionsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('RemoveRecurringWeatherActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        recurringAction = await self.__recurringActionsRepository.getWeatherRecurringAction(
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        if recurringAction is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Your channel has no recurring weather action',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        elif not recurringAction.isEnabled:
            self.__twitchChatMessenger.send(
                text = f'⚠ Your channel\'s recurring weather action is already disabled',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        await self.__recurringActionsHelper.disableRecurringAction(
            recurringAction = recurringAction,
        )

        self.__twitchChatMessenger.send(
            text = f'ⓘ Recurring weather action has been disabled',
            twitchChannelId = await ctx.getTwitchChannelId(),
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('RemoveRecurringWeatherActionCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
