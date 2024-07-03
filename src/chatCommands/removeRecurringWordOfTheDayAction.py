from .absChatCommand import AbsChatCommand
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..recurringActions.recurringActionsHelperInterface import \
    RecurringActionsHelperInterface
from ..recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class RemoveRecurringWordOfTheDayActionCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        recurringActionsHelper: RecurringActionsHelperInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(recurringActionsHelper, RecurringActionsHelperInterface):
            raise TypeError(f'recurringActionsHelper argument is malformed: \"{recurringActionsHelper}\"')
        elif not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__recurringActionsHelper: RecurringActionsHelperInterface = recurringActionsHelper
        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('RemoveWordOfTheDayRecurringActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        recurringAction = await self.__recurringActionsRepository.getWordOfTheDayRecurringAction(
            twitchChannel = user.getHandle(),
            twitchChannelId = userId
        )

        if recurringAction is None:
            await self.__twitchUtils.safeSend(ctx, f'⚠ Your channel has no recurring word of the day action')
            return
        elif not recurringAction.isEnabled():
            await self.__twitchUtils.safeSend(ctx, f'⚠ Your channel\'s recurring word of the day action is already disabled')
            return

        await self.__recurringActionsHelper.disableRecurringAction(recurringAction)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Recurring word of the day action has been disabled')
        self.__timber.log('RemoveWordOfTheDayRecurringActionCommand', f'Handled !removewordofthedayrecurringaction command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
