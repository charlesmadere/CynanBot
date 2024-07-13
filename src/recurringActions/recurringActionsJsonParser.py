import json
from typing import Any

from .recurringAction import RecurringAction
from .recurringActionType import RecurringActionType
from .recurringActionsJsonParserInterface import RecurringActionsJsonParserInterface
from .superTriviaRecurringAction import SuperTriviaRecurringAction
from .weatherRecurringAction import WeatherRecurringAction
from .wordOfTheDayRecurringAction import WordOfTheDayRecurringAction
from ..language.languageEntry import LanguageEntry
from ..language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class RecurringActionsJsonParser(RecurringActionsJsonParserInterface):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__timber: TimberInterface = timber

    async def parseActionType(
        self,
        actionType: str | Any | None
    ) -> RecurringActionType | None:
        if not utils.isValidStr(actionType):
            return None

        actionType = actionType.lower()

        match actionType:
            case 'super_trivia': return RecurringActionType.SUPER_TRIVIA
            case 'weather': return RecurringActionType.WEATHER
            case 'word_of_the_day': return RecurringActionType.WORD_OF_THE_DAY
            case _:
                self.__timber.log('RecurringActionsJsonParser', f'Encountered unknown RecurringActionType value: \"{actionType}\"')
                return None

    async def parseSuperTrivia(
        self,
        enabled: bool,
        minutesBetween: int | None,
        jsonString: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> SuperTriviaRecurringAction | None:
        if not utils.isValidStr(jsonString):
            return None

        return SuperTriviaRecurringAction(
            enabled = enabled,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            minutesBetween = minutesBetween
        )

    async def parseWeather(
        self,
        enabled: bool,
        minutesBetween: int | None,
        jsonString: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> WeatherRecurringAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] | None = json.loads(jsonString)

        alertsOnly = utils.getBoolFromDict(
            d = jsonContents,
            key = 'alertsOnly',
            fallback = True
        )

        return WeatherRecurringAction(
            alertsOnly = alertsOnly,
            enabled = enabled,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            minutesBetween = minutesBetween
        )

    async def parseWordOfTheDay(
        self,
        enabled: bool,
        minutesBetween: int | None,
        jsonString: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> WordOfTheDayRecurringAction | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: dict[str, Any] | None = json.loads(jsonString)

        wotdApiCode = utils.getStrFromDict(
            d = jsonContents,
            key = 'languageEntry',
            fallback = ''
        )

        languageEntry: LanguageEntry | None = None

        if utils.isValidStr(wotdApiCode):
            languageEntry = await self.__languagesRepository.getLanguageForWotdApiCode(wotdApiCode)

            if languageEntry is None:
                self.__timber.log('RecurringActionsJsonParser', f'Unable to find language for Word of the Day API code ({wotdApiCode=}) ({jsonContents=})')

        return WordOfTheDayRecurringAction(
            enabled = enabled,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            minutesBetween = minutesBetween,
            languageEntry = languageEntry
        )

    async def serializeActionType(
        self,
        actionType: RecurringActionType
    ) -> str:
        if not isinstance(actionType, RecurringActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')

        match actionType:
            case RecurringActionType.SUPER_TRIVIA: return 'super_trivia'
            case RecurringActionType.WEATHER: return 'weather'
            case RecurringActionType.WORD_OF_THE_DAY: return 'word_of_the_day'
            case _: raise ValueError(f'Encountered unknown RecurringActionType: \"{actionType}\"')

    async def __superTriviaToJson(self, action: SuperTriviaRecurringAction) -> str:
        if not isinstance(action, SuperTriviaRecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        jsonContents: dict[str, Any] = dict()
        return json.dumps(jsonContents)

    async def toJson(self, action: RecurringAction) -> str:
        if not isinstance(action, RecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if isinstance(action, SuperTriviaRecurringAction):
            return await self.__superTriviaToJson(action)
        elif isinstance(action, WeatherRecurringAction):
            return await self.__weatherToJson(action)
        elif isinstance(action, WordOfTheDayRecurringAction):
            return await self.__wordOfTheDayToJson(action)
        else:
            raise ValueError(f'Encountered unknown RecurringAction type ({action=})')

    async def __weatherToJson(self, action: WeatherRecurringAction) -> str:
        if not isinstance(action, WeatherRecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        jsonContents: dict[str, Any] = {
            'alertsOnly': action.isAlertsOnly
        }

        return json.dumps(jsonContents)

    async def __wordOfTheDayToJson(self, action: WordOfTheDayRecurringAction) -> str:
        if not isinstance(action, WordOfTheDayRecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        languageEntry = action.languageEntry
        jsonContents: dict[str, Any] = dict()

        if languageEntry is not None and utils.isValidStr(languageEntry.wotdApiCode):
            jsonContents['languageEntry'] = languageEntry.wotdApiCode

        return json.dumps(jsonContents)
