from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.recurringActions.recurringActionsWizardInterface import \
    RecurringActionsWizardInterface
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.superTriviaStep import SuperTriviaStep
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class AddRecurringSuperTriviaActionChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        recurringActionsWizard: RecurringActionsWizardInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(recurringActionsWizard, RecurringActionsWizardInterface):
            raise TypeError(f'recurringActionsWizard argument is malformed: \"{recurringActionsWizard}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__recurringActionsWizard: RecurringActionsWizardInterface = recurringActionsWizard
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('AddRecurringSuperTriviaActionChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return
        elif not user.areRecurringActionsEnabled():
            return

        wizard = await self.__recurringActionsWizard.start(
            recurringActionType = RecurringActionType.SUPER_TRIVIA,
            twitchChannel = user.getHandle(),
            twitchChannelId = userId
        )

        step = wizard.getSteps().getStep()

        if step is SuperTriviaStep.MINUTES_BETWEEN:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Please specify the number of minutes between recurring Super Trivia questions (most people choose 20 - 45 minutes)')
        else:
            raise RuntimeError(f'unknown SuperTriviaStep: \"{step}\"')

        self.__timber.log('AddRecurringSuperTriviaActionChatCommand', f'Handled !addrecurringsupertriviaaction command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
