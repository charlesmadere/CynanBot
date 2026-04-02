import traceback
from typing import Final

from .absChatAction2 import AbsChatAction2
from .chatActionResult import ChatActionResult
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..recurringActions.actions.cutenessRecurringAction import CutenessRecurringAction
from ..recurringActions.actions.superTriviaRecurringAction import SuperTriviaRecurringAction
from ..recurringActions.actions.weatherRecurringAction import WeatherRecurringAction
from ..recurringActions.recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from ..recurringActions.recurringActionsWizardInterface import RecurringActionsWizardInterface
from ..recurringActions.wizards.cuteness.cutenessStep import CutenessStep
from ..recurringActions.wizards.cuteness.cutenessWizard import CutenessWizard
from ..recurringActions.wizards.stepResult import StepResult
from ..recurringActions.wizards.superTrivia.superTriviaStep import SuperTriviaStep
from ..recurringActions.wizards.superTrivia.superTriviaWizard import SuperTriviaWizard
from ..recurringActions.wizards.weather.weatherStep import WeatherStep
from ..recurringActions.wizards.weather.weatherWizard import WeatherWizard
from ..recurringActions.wizards.wordOfTheDay.wordOfTheDayWizard import WordOfTheDayWizard
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class RecurringActionsWizardChatAction(AbsChatAction2):

    def __init__(
        self,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        recurringActionsWizard: RecurringActionsWizardInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(recurringActionsWizard, RecurringActionsWizardInterface):
            raise TypeError(f'recurringActionsWizard argument is malformed: \"{recurringActionsWizard}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__recurringActionsRepository: Final[RecurringActionsRepositoryInterface] = recurringActionsRepository
        self.__recurringActionsWizard: Final[RecurringActionsWizardInterface] = recurringActionsWizard
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    @property
    def actionName(self) -> str:
        return 'RecurringActionsWizardChatAction'

    async def __configureCutenessWizard(
        self,
        wizard: CutenessWizard,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        steps = wizard.steps

        match steps.currentStep:
            case CutenessStep.MINUTES_BETWEEN:
                try:
                    minutesBetween = int(chatMessage.text)
                    wizard.setMinutesBetween(minutesBetween)
                except Exception as e:
                    self.__timber.log('RecurringActionsWizardChatAction', f'Unable to parse/set minutesBetween value for Cuteness wizard ({wizard=}) ({chatMessage=})', e, traceback.format_exc())
                    await self.__send(chatMessage, f'⚠ The Cuteness wizard encountered an error, please try again')
                    await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                    return ChatActionResult.HANDLED

        stepResult = steps.stepForward()

        match stepResult:
            case StepResult.DONE:
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)

                await self.__recurringActionsRepository.setRecurringAction(CutenessRecurringAction(
                    enabled = True,
                    twitchChannel = wizard.twitchChannel,
                    twitchChannelId = wizard.twitchChannelId,
                    minutesBetween = wizard.requireMinutesBetween(),
                ))

                self.__timber.log('RecurringActionsWizardChatAction', f'Finished configuring Cuteness wizard ({wizard=}) ({chatMessage=})')
                await self.__send(chatMessage, f'ⓘ Finished configuring Cuteness wizard ({wizard.printOut()})')
                return ChatActionResult.HANDLED

            case StepResult.NEXT:
                self.__timber.log('RecurringActionsWizardChatAction', f'Cuteness wizard is in an invalid state ({wizard=}) ({chatMessage=})')
                await self.__send(chatMessage, f'⚠ The Cuteness wizard is in an invalid state, please try again')
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                return ChatActionResult.HANDLED

    async def __configureSuperTriviaWizard(
        self,
        wizard: SuperTriviaWizard,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        steps = wizard.steps

        match steps.currentStep:
            case SuperTriviaStep.MINUTES_BETWEEN:
                try:
                    minutesBetween = int(chatMessage.text)
                    wizard.setMinutesBetween(minutesBetween)
                except Exception as e:
                    self.__timber.log('RecurringActionsWizardChatAction', f'Unable to parse/set minutesBetween value for Super Trivia wizard ({wizard=}) ({chatMessage=})', e, traceback.format_exc())
                    await self.__send(chatMessage, f'⚠ The Super Trivia wizard encountered an error, please try again')
                    await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                    return ChatActionResult.HANDLED

        stepResult = steps.stepForward()

        match stepResult:
            case StepResult.DONE:
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)

                await self.__recurringActionsRepository.setRecurringAction(SuperTriviaRecurringAction(
                    enabled = True,
                    twitchChannel = wizard.twitchChannel,
                    twitchChannelId = wizard.twitchChannelId,
                    minutesBetween = wizard.requireMinutesBetween(),
                ))

                self.__timber.log('RecurringActionsWizardChatAction', f'Finished configuring Super Trivia wizard ({wizard=}) ({chatMessage=})')
                await self.__send(chatMessage, f'ⓘ Finished configuring Super Trivia ({wizard.printOut()})')
                return ChatActionResult.HANDLED

            case StepResult.NEXT:
                self.__timber.log('RecurringActionsWizardChatAction', f'Super Trivia wizard is in an invalid state ({wizard=}) ({chatMessage=})')
                await self.__send(chatMessage, f'⚠ The Super Trivia wizard is in an invalid state, please try again')
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                return ChatActionResult.HANDLED

    async def __configureWeatherWizard(
        self,
        chatMessage: TwitchChatMessage,
        wizard: WeatherWizard,
    ) -> ChatActionResult:
        steps = wizard.steps

        match steps.currentStep:
            case WeatherStep.MINUTES_BETWEEN:
                try:
                    minutesBetween = int(chatMessage.text)
                    wizard.setMinutesBetween(minutesBetween)
                except Exception as e:
                    self.__timber.log('RecurringActionsWizardChatAction', f'Unable to parse/set minutesBetween value for Weather wizard ({wizard=}) ({chatMessage=})', e, traceback.format_exc())
                    await self.__send(chatMessage, f'⚠ The Weather wizard encountered an error, please try again')
                    await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                    return ChatActionResult.HANDLED

            case WeatherStep.ALERTS_ONLY:
                try:
                    alertsOnly = utils.strToBool(chatMessage.text)
                    wizard.setAlertsOnly(alertsOnly)
                except Exception as e:
                    self.__timber.log('RecurringActionsWizardChatAction', f'Unable to parse/set alertsOnly value for Weather wizard ({wizard=}) ({chatMessage=})', e, traceback.format_exc())
                    await self.__send(chatMessage, f'⚠ The Weather wizard encountered an error, please try again')
                    await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                    return ChatActionResult.HANDLED

        stepResult = steps.stepForward()

        match stepResult:
            case StepResult.DONE:
                await self.__recurringActionsWizard.complete(wizard.twitchChannelId)

                await self.__recurringActionsRepository.setRecurringAction(WeatherRecurringAction(
                    enabled = True,
                    twitchChannel = wizard.twitchChannel,
                    twitchChannelId = wizard.twitchChannelId,
                    alertsOnly = wizard.requireAlertsOnly(),
                    minutesBetween = wizard.requireMinutesBetween(),
                ))

                self.__timber.log('RecurringActionsWizardChatAction', f'Finished configuring Weather wizard ({wizard=}) ({chatMessage=})')
                await self.__send(chatMessage, f'ⓘ Finished configuring Weather wizard ({wizard.printOut()})')
                return ChatActionResult.HANDLED

            case StepResult.NEXT:
                match steps.currentStep:
                    case WeatherStep.ALERTS_ONLY:
                        await self.__send(chatMessage, f'ⓘ Please specify if Weather prompts are for Alerts Only (the default is True)')
                        return ChatActionResult.HANDLED

                    case _:
                        self.__timber.log('RecurringActionsWizardChatAction', f'Weather wizard is in an invalid state ({wizard=}) ({chatMessage=})')
                        await self.__send(chatMessage, f'⚠ The Weather wizard is in an invalid state, please try again')
                        await self.__recurringActionsWizard.complete(wizard.twitchChannelId)
                        return ChatActionResult.HANDLED

    async def __configureWordOfTheDayWizard(
        self,
        chatMessage: TwitchChatMessage,
        wizard: WordOfTheDayWizard,
    ) -> ChatActionResult:
        # TODO
        return ChatActionResult.IGNORED

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        wizard = await self.__recurringActionsWizard.get(chatMessage.twitchChannelId)

        if wizard is None or not utils.isValidStr(chatMessage.text) or chatMessage.twitchChannelId != chatMessage.chatterUserId:
            return ChatActionResult.IGNORED

        if isinstance(wizard, CutenessWizard):
            return await self.__configureCutenessWizard(
                wizard = wizard,
                chatMessage = chatMessage,
            )

        elif isinstance(wizard, SuperTriviaWizard):
            return await self.__configureSuperTriviaWizard(
                wizard = wizard,
                chatMessage = chatMessage,
            )

        elif isinstance(wizard, WeatherWizard):
            return await self.__configureWeatherWizard(
                chatMessage = chatMessage,
                wizard = wizard,
            )

        elif isinstance(wizard, WordOfTheDayWizard):
            return await self.__configureWordOfTheDayWizard(
                chatMessage = chatMessage,
                wizard = wizard,
            )

        else:
            self.__timber.log(self.actionName, f'Encountered unknown AbsWizard type ({wizard=}) ({chatMessage=})')
            await self.__recurringActionsWizard.complete(chatMessage.twitchChannelId)
            return ChatActionResult.IGNORED

    async def __send(self, chatMessage: TwitchChatMessage, chat: str):
        self.__twitchChatMessenger.send(
            text = chat,
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )
