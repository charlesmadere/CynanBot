import traceback

from .absChatAction import AbsChatAction
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..recurringActions.cutenessRecurringAction import CutenessRecurringAction
from ..recurringActions.recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from ..recurringActions.recurringActionsWizardInterface import RecurringActionsWizardInterface
from ..recurringActions.superTriviaRecurringAction import SuperTriviaRecurringAction
from ..recurringActions.weatherRecurringAction import WeatherRecurringAction
from ..recurringActions.wizards.cutenessStep import CutenessStep
from ..recurringActions.wizards.cutenessWizard import CutenessWizard
from ..recurringActions.wizards.stepResult import StepResult
from ..recurringActions.wizards.superTriviaStep import SuperTriviaStep
from ..recurringActions.wizards.superTriviaWizard import SuperTriviaWizard
from ..recurringActions.wizards.weatherStep import WeatherStep
from ..recurringActions.wizards.weatherWizard import WeatherWizard
from ..recurringActions.wizards.wordOfTheDayWizard import WordOfTheDayWizard
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userInterface import UserInterface


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

    async def __configureCutenessWizard(
        self,
        wizard: CutenessWizard,
        content: str,
        message: TwitchMessage
    ) -> bool:
        channel = message.getChannel()
        steps = wizard.getSteps()
        step = steps.getStep()

        match step:
            case CutenessStep.MINUTES_BETWEEN:
                try:
                    minutesBetween = int(content)
                    wizard.setMinutesBetween(minutesBetween)
                except Exception as e:
                    self.__timber.log('RecurringActionsWizardChatAction', f'Unable to parse/set minutesBetween value for Cuteness wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Cuteness wizard encountered an error, please try again')
                    await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                    return True

            case _:
                self.__timber.log('CheerActionsWizardChatAction', f'The Cuteness wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Cuteness wizard is in an invalid state, please try again')
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                return True

        stepResult = steps.stepForward()

        match stepResult:
            case StepResult.DONE:
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)

                await self.__recurringActionsRepository.setRecurringAction(CutenessRecurringAction(
                    enabled = True,
                    twitchChannel = wizard.twitchChannel,
                    twitchChannelId = wizard.twitchChannelId,
                    minutesBetween = wizard.requireMinutesBetween()
                ))

                self.__timber.log('RecurringActionsWizardChatAction', f'Finished configuring Cuteness wizard ({message.getAuthorId()=}) ({message.getAuthorName()=}) ({message.getTwitchChannelName()=})')
                await self.__twitchUtils.safeSend(channel, f'ⓘ Finished configuring Cuteness wizard ({wizard.printOut()})')
                return True

            case StepResult.NEXT:
                self.__timber.log('RecurringActionsWizardChatAction', f'Cuteness wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Cuteness wizard is in an invalid state, please try again')
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                return True

            case _:
                self.__timber.log('RecurringActionsWizardChatAction', f'Cuteness wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Cuteness wizard is in an invalid state, please try again')
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                return True

    async def __configureSuperTriviaWizard(
        self,
        content: str,
        wizard: SuperTriviaWizard,
        message: TwitchMessage
    ) -> bool:
        channel = message.getChannel()
        steps = wizard.getSteps()
        step = steps.getStep()

        match step:
            case SuperTriviaStep.MINUTES_BETWEEN:
                try:
                    minutesBetween = int(content)
                    wizard.setMinutesBetween(minutesBetween)
                except Exception as e:
                    self.__timber.log('RecurringActionsWizardChatAction', f'Unable to parse/set minutesBetween value for Super Trivia wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Super Trivia wizard encountered an error, please try again')
                    await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                    return True

            case _:
                self.__timber.log('RecurringActionsWizardChatAction', f'The Super Trivia wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Super Trivia wizard is in an invalid state, please try again')
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                return True

        stepResult = steps.stepForward()

        match stepResult:
            case StepResult.DONE:
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)

                await self.__recurringActionsRepository.setRecurringAction(SuperTriviaRecurringAction(
                    enabled = True,
                    twitchChannel = wizard.twitchChannel,
                    twitchChannelId = wizard.twitchChannelId,
                    minutesBetween = wizard.requireMinutesBetween()
                ))

                self.__timber.log('RecurringActionsWizardChatAction', f'Finished configuring Super Trivia wizard ({message.getAuthorId()=}) ({message.getAuthorName()=}) ({message.getTwitchChannelName()=})')
                await self.__twitchUtils.safeSend(channel, f'ⓘ Finished configuring Super Trivia ({wizard.printOut()})')
                return True

            case StepResult.NEXT:
                self.__timber.log('RecurringActionsWizardChatAction', f'Super Trivia wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Super Trivia wizard is in an invalid state, please try again')
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                return True

            case _:
                self.__timber.log('RecurringActionsWizardChatAction', f'Super Trivia wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Super Trivia wizard is in an invalid state, please try again')
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                return True

    async def __configureWeatherWizard(
        self,
        content: str,
        message: TwitchMessage,
        wizard: WeatherWizard
    ) -> bool:
        channel = message.getChannel()
        steps = wizard.getSteps()
        step = steps.getStep()

        match step:
            case WeatherStep.MINUTES_BETWEEN:
                try:
                    minutesBetween = int(content)
                    wizard.setMinutesBetween(minutesBetween)
                except Exception as e:
                    self.__timber.log('RecurringActionsWizardChatAction', f'Unable to parse/set minutesBetween value for Weather wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Weather wizard encountered an error, please try again')
                    await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                    return True

            case WeatherStep.ALERTS_ONLY:
                try:
                    alertsOnly = utils.strToBool(content)
                    wizard.setAlertsOnly(alertsOnly)
                except Exception as e:
                    self.__timber.log('RecurringActionsWizardChatAction', f'Unable to parse/set alertsOnly value for Weather wizard ({wizard=}) ({content=}): {e}', e, traceback.format_exc())
                    await self.__twitchUtils.safeSend(channel, f'⚠ The Weather wizard encountered an error, please try again')
                    await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                    return True
            case _:
                self.__timber.log('RecurringActionsWizardChatAction', f'The Weather wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Weather wizard is in an invalid state, please try again')
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                return True

        stepResult = steps.stepForward()
        step = steps.getStep()

        match stepResult:
            case StepResult.DONE:
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)

                await self.__recurringActionsRepository.setRecurringAction(WeatherRecurringAction(
                    enabled = True,
                    twitchChannel = wizard.twitchChannel,
                    twitchChannelId = wizard.twitchChannelId,
                    alertsOnly = wizard.requireAlertsOnly(),
                    minutesBetween = wizard.requireMinutesBetween()
                ))

                self.__timber.log('RecurringActionsWizardChatAction', f'Finished configuring Weather wizard ({message.getAuthorId()=}) ({message.getAuthorName()=}) ({message.getTwitchChannelName()=})')
                await self.__twitchUtils.safeSend(channel, f'ⓘ Finished configuring Weather wizard ({wizard.printOut()})')
                return True

            case StepResult.NEXT:
                match step:
                    case WeatherStep.ALERTS_ONLY:
                        await self.__twitchUtils.safeSend(channel, f'ⓘ Please specify if Weather prompts are for Alerts Only (the default is True)')
                        return True
                    case _:
                        self.__timber.log('RecurringActionsWizardChatAction', f'Weather wizard is in an invalid state ({wizard=})')
                        await self.__twitchUtils.safeSend(channel, f'⚠ The Weather wizard is in an invalid state, please try again')
                        await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                        return True
            case _:
                self.__timber.log('RecurringActionsWizardChatAction', f'Weather wizard is in an invalid state ({wizard=})')
                await self.__twitchUtils.safeSend(channel, f'⚠ The Weather wizard is in an invalid state, please try again')
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                return True

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

        if isinstance(wizard, CutenessWizard):
            return await self.__configureCutenessWizard(
                wizard = wizard,
                content = content,
                message = message
            )
        elif isinstance(wizard, SuperTriviaWizard):
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
