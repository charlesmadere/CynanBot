from typing import Optional

from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.recurringActions.recurringActionsWizardInterface import \
    RecurringActionsWizardInterface
from CynanBot.recurringActions.wizards.superTriviaStep import SuperTriviaStep
from CynanBot.recurringActions.wizards.superTriviaSteps import SuperTriviaSteps
from CynanBot.recurringActions.wizards.superTriviaWizard import \
    SuperTriviaWizard
from CynanBot.recurringActions.wizards.weatherWizard import WeatherWizard
from CynanBot.recurringActions.wizards.wordOfTheDayWizard import \
    WordOfTheDayWizard
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userInterface import UserInterface


class RecurringActionsWizardChatAction(AbsChatAction):

    def __init__(
        self,
        recurringActionsWizard: RecurringActionsWizardInterface,
        timber: TimberInterface
    ):
        if not isinstance(recurringActionsWizard, RecurringActionsWizardInterface):
            raise TypeError(f'recurringActionsWizard argument is malformed: \"{recurringActionsWizard}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__recurringActionsWizard: RecurringActionsWizardInterface = recurringActionsWizard
        self.__timber: TimberInterface = timber

    async def __configureSuperTriviaWizard(
        self,
        message: TwitchMessage,
        wizard: SuperTriviaWizard
    ) -> bool:
        steps = wizard.getSteps()
        step = steps.getStep()

        if step is SuperTriviaStep.MINUTES_BETWEEN:
            # TODO
            pass

        return False

    async def __configureWeatherWizard(
        self,
        message: TwitchMessage,
        wizard: WeatherWizard
    ) -> bool:
        return False

    async def __configureWordOfTheDayWizard(
        self,
        message: TwitchMessage,
        wizard: WordOfTheDayWizard
    ) -> bool:
        return False

    async def handleChat(
        self,
        mostRecentChat: Optional[MostRecentChat],
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        twitchChannelId = await message.getTwitchChannelId()
        wizard = await self.__recurringActionsWizard.get(twitchChannelId)

        if wizard is None or twitchChannelId != message.getAuthorId():
            return False

        if isinstance(wizard, SuperTriviaWizard):
            return await self.__configureSuperTriviaWizard(
                message = message,
                wizard = wizard
            )
        elif isinstance(wizard, WeatherWizard):
            return await self.__configureWeatherWizard(
                message = message,
                wizard = wizard
            )
        elif isinstance(wizard, WordOfTheDayWizard):
            return await self.__configureWordOfTheDayWizard(
                message = message,
                wizard = wizard
            )
        else:
            return False
