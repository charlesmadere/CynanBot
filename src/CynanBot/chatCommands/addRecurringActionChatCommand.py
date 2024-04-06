import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from CynanBot.recurringActions.recurringActionsWizardInterface import \
    RecurringActionsWizardInterface
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.superTriviaStep import SuperTriviaStep
from CynanBot.recurringActions.wizards.superTriviaWizard import \
    SuperTriviaWizard
from CynanBot.recurringActions.wizards.weatherWizard import WeatherWizard
from CynanBot.recurringActions.wizards.wordOfTheDayWizard import \
    WordOfTheDayWizard
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class AddRecurringActionChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        languagesRepository: LanguagesRepositoryInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        recurringActionsWizard: RecurringActionsWizardInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
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
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__recurringActionsWizard: RecurringActionsWizardInterface = recurringActionsWizard
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __announceCurrentSuperTriviaStep(self, ctx: TwitchContext, wizard: SuperTriviaWizard):
        step = wizard.getSteps().getStep()

        if step is SuperTriviaStep.MINUTES_BETWEEN:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Please specify the number of minutes between recurring Super Trivia questions (most people choose 20 - 30 minutes)')
        else:
            raise RuntimeError(f'unknown SuperTriviaStep: \"{step}\"')

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('AddRecurringActionChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return
        elif not user.areRecurringActionsEnabled():
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddRecurringActionChatCommand', f'No argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            await self.__twitchUtils.safeSend(ctx, f'⚠ One argument is necessary for the !addrecurringaction command. Example: !addrecurringaction supertrivia')
            return

        try:
            recurringActionType = RecurringActionType.fromStr(splits[1])
        except Exception as e:
            self.__timber.log('AddRecurringActionChatCommand', f'Unknown RecurringActionType value (\"{splits[1]}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to parse recurring action type for the !addrecurringaction command. Example: !addrecurringaction supertrivia')
            return

        wizard = await self.__recurringActionsWizard.start(
            recurringActionType = recurringActionType,
            twitchChannel = user.getHandle(),
            twitchChannelId = userId
        )

        if isinstance(wizard, SuperTriviaWizard):
            await self.__announceCurrentSuperTriviaStep(ctx, wizard)
        elif isinstance(wizard, WeatherWizard):
            # TODO
            pass
        elif isinstance(wizard, WordOfTheDayWizard):
            # TODO
            pass

        # TODO
        self.__timber.log('AddRecurringActionChatCommand', f'Handled !addrecurringaction command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
