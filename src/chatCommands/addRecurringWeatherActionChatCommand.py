from .absChatCommand import AbsChatCommand
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..recurringActions.actions.recurringActionType import RecurringActionType
from ..recurringActions.recurringActionsWizardInterface import RecurringActionsWizardInterface
from ..recurringActions.wizards.weather.weatherStep import WeatherStep
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AddRecurringWeatherActionChatCommand(AbsChatCommand):

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
            self.__timber.log('AddRecurringWeatherActionChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return
        elif not user.areRecurringActionsEnabled:
            return

        wizard = await self.__recurringActionsWizard.start(
            recurringActionType = RecurringActionType.WEATHER,
            twitchChannel = user.handle,
            twitchChannelId = userId
        )

        step = wizard.currentStep

        if step is not WeatherStep.MINUTES_BETWEEN:
            raise RuntimeError(f'unknown WeatherStep: \"{step}\"')

        minimumRecurringActionTimingMinutes = RecurringActionType.WEATHER.minimumRecurringActionTimingMinutes

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'ⓘ Please specify the number of minutes between recurring Weather prompts (most people choose 60 - 120 minutes, minimum is {minimumRecurringActionTimingMinutes})',
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('AddRecurringWeatherActionChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
