from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from CynanBot.recurringActions.recurringActionsWizardInterface import \
    RecurringActionsWizardInterface
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.weatherStep import WeatherStep
from CynanBot.recurringActions.wizards.weatherWizard import WeatherWizard
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class SetWeatherRecurringActionCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        recurringActionsWizard: RecurringActionsWizardInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(recurringActionsWizard, RecurringActionsWizardInterface):
            raise TypeError(f'recurringActionsWizard argument is malformed: \"{recurringActionsWizard}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__recurringActionsWizard: RecurringActionsWizardInterface = recurringActionsWizard
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __beginWizardGuidance(self, ctx: TwitchContext, wizard: WeatherWizard):
        if wizard.getSteps().getStep() is WeatherStep.ALERTS_ONLY:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Please specify if weather reports should only show if your region has a critical alert or warning')
        elif wizard.getSteps().getStep() is WeatherStep.MINUTES_BETWEEN:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Please specify the number of minutes between each weather report')
        else:
            self.__timber.log('SetWeatherRecurringActionCommand', f'Received invalid wizard step: \"{wizard}\" ({ctx.getAuthorName()=}) ({ctx.getAuthorId()}) ({ctx.getTwitchChannelName()})')

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('SetWeatherRecurringActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        wizard = await self.__recurringActionsWizard.start(
            recurringActionType = RecurringActionType.WEATHER,
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if not isinstance(wizard, WeatherWizard):
            # this should be impossible, I'm mostly just using this for a type check
            self.__timber.log('SetWeatherRecurringActionCommand', f'Received incorrect wizard instance: \"{wizard}\" ({ctx.getAuthorName()=}) ({ctx.getAuthorId()=}) ({ctx.getTwitchChannelName()=})')
            return

        await self.__beginWizardGuidance(
            ctx = ctx,
            wizard = wizard
        )
