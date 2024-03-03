from datetime import timedelta
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.timedDict import TimedDict
from CynanBot.recurringActions.recurringActionsWizardInterface import \
    RecurringActionsWizardInterface
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.superTriviaWizard import \
    SuperTriviaWizard
from CynanBot.recurringActions.wizards.weatherWizard import WeatherWizard
from CynanBot.recurringActions.wizards.wordOfTheDayWizard import \
    WordOfTheDayWizard
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface


class RecurringActionsWizard(RecurringActionsWizardInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        timePerStep: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(timePerStep, timedelta):
            raise TypeError(f'timePerStep argument is malformed: \"{timePerStep}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__timePerStep: timedelta = timePerStep

        self.__wizards: TimedDict = TimedDict(timePerStep)
        self.__twitchChannelProvider: Optional[TwitchChannelProvider] = None

    def setTwitchChannelProvider(self, twitchChannelProvider: Optional[TwitchChannelProvider]):
        if twitchChannelProvider is not None and not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise TypeError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')

        self.__twitchChannelProvider = twitchChannelProvider

    async def start(
        self,
        recurringActionType: RecurringActionType,
        twitchChannel: str,
        twitchChannelId: str
    ):
        if not isinstance(recurringActionType, RecurringActionType):
            raise TypeError(f'recurringActionType argument is malformed: \"{recurringActionType}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            self.__timber.log('RecurringActionsWizard', f'Attempted to start, but twitchChannelProvider is None ({recurringActionType=}) ({twitchChannel=}) ({twitchChannelId=}) ({twitchChannelProvider=})')
            return

        existingStep = self.__wizards[twitchChannelId]

        if existingStep is not None:
            self.__timber.log('RecurringActionsWizard', f'Starting a new \"{recurringActionType}\" wizard for {twitchChannel}:{twitchChannelId}, but an existing step was found: \"{existingStep}\"')

        await self.__startNewWizard(
            recurringActionType = recurringActionType,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    async def __startNewSuperTriviaWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__wizards[twitchChannelId] = SuperTriviaWizard()

    async def __startNewWeatherWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__wizards[twitchChannelId] = WeatherWizard()

    async def __startNewWizard(
        self,
        recurringActionType: RecurringActionType,
        twitchChannel: str,
        twitchChannelId: str
    ):
        if not isinstance(recurringActionType, RecurringActionType):
            raise TypeError(f'recurringActionType argument is malformed: \"{recurringActionType}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if recurringActionType is RecurringActionType.SUPER_TRIVIA:
            await self.__startNewSuperTriviaWizard(
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )
        elif recurringActionType is RecurringActionType.WEATHER:
            await self.__startNewWeatherWizard(
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )
        elif recurringActionType is RecurringActionType.WORD_OF_THE_DAY:
            await self.__startNewWordOfTheDayWizard(
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )
        else:
            raise RuntimeError(f'unknown RecurringActionType: \"{recurringActionType}\"')

    async def __startNewWordOfTheDayWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__wizards[twitchChannelId] = WordOfTheDayWizard()
