import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from CynanBot.recurringActions.recurringActionsWizardInterface import \
    RecurringActionsWizardInterface
from CynanBot.recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from CynanBot.recurringActions.wizards.stepResult import StepResult
from CynanBot.recurringActions.wizards.superTriviaStep import SuperTriviaStep
from CynanBot.recurringActions.wizards.superTriviaWizard import \
    SuperTriviaWizard
from CynanBot.recurringActions.wizards.weatherWizard import WeatherWizard
from CynanBot.recurringActions.wizards.wordOfTheDayWizard import \
    WordOfTheDayWizard
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userInterface import UserInterface


class RecurringActionsWizardChatAction(AbsChatAction):

    def __init__(
        self,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        recurringActionsWizard: RecurringActionsWizardInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        if not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(recurringActionsWizard, RecurringActionsWizardInterface):
            raise TypeError(f'recurringActionsWizard argument is malformed: \"{recurringActionsWizard}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__recurringActionsWizard: RecurringActionsWizardInterface = recurringActionsWizard
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def __configureSuperTriviaWizard(
        self,
        content: str,
        wizard: SuperTriviaWizard,
        message: TwitchMessage
    ) -> bool:
        channel = message.getChannel()
        steps = wizard.getSteps()
        step = steps.getStep()

        if step is not SuperTriviaStep.MINUTES_BETWEEN:
            # this situation should be impossible for super trivia
            self.__timber.log('RecurringActionsWizardChatAction', f'Super Trivia wizard is at an invalid step: ({content=}) ({step=}) ({message.getAuthorId()=}) ({message.getAuthorName()=}) ({message.getTwitchChannelName()=})')
            await self.__twitchUtils.safeSend(channel, f'⚠ The Super Trivia wizard is in an invalid state, please try again')
            await self.__recurringActionsWizard.complete(await channel.getTwitchChannelId())
            return True

        minutesBetween = utils.safeStrToInt(content)

        if not utils.isValidInt(minutesBetween) or minutesBetween < 1 or minutesBetween > utils.getIntMaxSafeSize():
            self.__timber.log('RecurringActionsWizardChatAction', f'Super Trivia wizard was given illegal minutesBetween value: ({content=}) ({step=}) ({minutesBetween=}) ({message.getAuthorId()=}) ({message.getAuthorName()=}) ({message.getTwitchChannelName()=})')
            await self.__twitchUtils.safeSend(channel, f'⚠ The given \"minutes between\" value is malformed, please start over with recurring Super Trivia configuration')
            await self.__recurringActionsWizard.complete(await channel.getTwitchChannelId())
            return True

        wizard.setMinutesBetween(minutesBetween)

        if steps.stepForward() is not StepResult.DONE:
            # this situation should be impossible for super trivia
            self.__timber.log('RecurringActionsWizardChatAction', f'Super Trivia wizard was unable to step forward: ({content=}) ({step=}) ({minutesBetween=}) ({message.getAuthorId()=}) ({message.getAuthorName()=}) ({message.getTwitchChannelName()=})')
            await self.__twitchUtils.safeSend(channel, f'⚠ The Super Trivia wizard is in an invalid state, please try again')
            await self.__recurringActionsWizard.complete(await channel.getTwitchChannelId())
            return True

        await self.__recurringActionsRepository.setRecurringAction(SuperTriviaRecurringAction(
            enabled = True,
            twitchChannel = channel.getTwitchChannelName(),
            minutesBetween = wizard.getMinutesBetween()
        ))

        self.__timber.log('RecurringActionsWizardChatAction', f'Finished configuring Super Trivia wizard ({message.getAuthorId()=}) ({message.getAuthorName()=}) ({message.getTwitchChannelName()=})')
        await self.__twitchUtils.safeSend(channel, f'ⓘ Finished configuring recurring Super Trivia (minutes between: {wizard.getMinutesBetween()})')
        return True

    async def __configureWeatherWizard(
        self,
        content: str,
        message: TwitchMessage,
        wizard: WeatherWizard
    ) -> bool:
        # TODO
        return False

    async def __configureWordOfTheDayWizard(
        self,
        content: str,
        message: TwitchMessage,
        wizard: WordOfTheDayWizard
    ) -> bool:
        # TODO
        return False

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        content = message.getContent()
        twitchChannelId = await message.getTwitchChannelId()
        wizard = await self.__recurringActionsWizard.get(twitchChannelId)

        if not utils.isValidStr(content) or twitchChannelId != message.getAuthorId() or wizard is None:
            return False

        if isinstance(wizard, SuperTriviaWizard):
            return await self.__configureSuperTriviaWizard(
                content = content,
                wizard = wizard,
                message = message
            )
        elif isinstance(wizard, WeatherWizard):
            return await self.__configureWeatherWizard(
                content = content,
                message = message,
                wizard = wizard
            )
        elif isinstance(wizard, WordOfTheDayWizard):
            return await self.__configureWordOfTheDayWizard(
                content = content,
                message = message,
                wizard = wizard
            )
        else:
            self.__timber.log('RecurringActionsWizardChatAction', f'Received unknown AbsWizard type: \"{wizard}\" ({message.getAuthorName()=}) ({message.getAuthorName()=}) ({twitchChannelId=}) ({message.getTwitchChannelName()=})')
            return False
