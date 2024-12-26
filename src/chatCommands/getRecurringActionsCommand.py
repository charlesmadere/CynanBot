from .absChatCommand import AbsChatCommand
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..recurringActions.actions.recurringAction import RecurringAction
from ..recurringActions.recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class GetRecurringActionsCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', '
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('GetRecurringActionsCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        recurringActions = await self.__recurringActionsRepository.getAllRecurringActions(
            twitchChannel = user.handle,
            twitchChannelId = userId
        )

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = await self.__toStr(recurringActions),
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('GetRecurringActionsCommand', f'Handled !getrecurringactions command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

    async def __toStr(self, recurringActions: list[RecurringAction]) -> str:
        if not isinstance(recurringActions, list):
            raise TypeError(f'recurringActions argument is malformed: \"{recurringActions}\"')

        if len(recurringActions) == 0:
            return 'ⓘ Your channel has no recurring actions'

        recurringActionsStrs: list[str] = list()

        for recurringAction in recurringActions:
            recurringActionsStrs.append(recurringAction.actionType.humanReadableString)

        recurringActionsStr = self.__delimiter.join(recurringActionsStrs)
        return f'ⓘ Your channel\'s recurring action(s): {recurringActionsStr}'
