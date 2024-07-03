from datetime import timedelta

from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from .recurringActionsWizardInterface import \
    RecurringActionsWizardInterface
from .recurringActionType import RecurringActionType
from .wizards.absWizard import AbsWizard
from .wizards.superTriviaWizard import SuperTriviaWizard
from .wizards.weatherWizard import WeatherWizard
from .wizards.wordOfTheDayWizard import WordOfTheDayWizard
from ..timber.timberInterface import TimberInterface


class RecurringActionsWizard(RecurringActionsWizardInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timePerStep: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timePerStep, timedelta):
            raise TypeError(f'timePerStep argument is malformed: \"{timePerStep}\"')

        self.__timber: TimberInterface = timber
        self.__wizards: TimedDict[AbsWizard] = TimedDict(timePerStep)

    async def complete(self, twitchChannelId: str):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        del self.__wizards[twitchChannelId]

    async def get(self, twitchChannelId: str) -> AbsWizard | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        return self.__wizards[twitchChannelId]

    async def start(
        self,
        recurringActionType: RecurringActionType,
        twitchChannel: str,
        twitchChannelId: str
    ) -> AbsWizard:
        if not isinstance(recurringActionType, RecurringActionType):
            raise TypeError(f'recurringActionType argument is malformed: \"{recurringActionType}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        existingWizard = self.__wizards[twitchChannelId]

        if existingWizard is not None:
            self.__timber.log('RecurringActionsWizard', f'Starting a new \"{recurringActionType}\" wizard for {twitchChannel}:{twitchChannelId}, which will clobber an existing wizard: \"{existingWizard}\"')

        match recurringActionType:
            case RecurringActionType.SUPER_TRIVIA:
                return await self.__startNewSuperTriviaWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId
                )

            case RecurringActionType.WEATHER:
                return await self.__startNewWeatherWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId
                )

            case RecurringActionType.WORD_OF_THE_DAY:
                return await self.__startNewWordOfTheDayWizard(
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId
                )

            case _:
                raise RuntimeError(f'unknown RecurringActionType: \"{recurringActionType}\"')

    async def __startNewSuperTriviaWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> SuperTriviaWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = SuperTriviaWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('RecurringActionsWizard', f'Started new Super Trivia wizard for {twitchChannel}:{twitchChannelId}')

        return wizard

    async def __startNewWeatherWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> WeatherWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = WeatherWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('RecurringActionsWizard', f'Started new Weather wizard for {twitchChannel}:{twitchChannelId}')

        return wizard

    async def __startNewWordOfTheDayWizard(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> WordOfTheDayWizard:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        wizard = WordOfTheDayWizard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__wizards[twitchChannelId] = wizard
        self.__timber.log('RecurringActionsWizard', f'Started new Word Of The Day wizard for {twitchChannel}:{twitchChannelId}')

        return wizard
