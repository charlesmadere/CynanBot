import json
from typing import Any, Dict, Optional

import misc.utils as utils
from language.languagesRepository import LanguagesRepository
from recurringActions.recurringAction import RecurringAction
from recurringActions.recurringActionsJsonParserInterface import \
    RecurringActionsJsonParserInterface
from recurringActions.recurringActionType import RecurringActionType
from recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from recurringActions.weatherRecurringAction import WeatherRecurringAction
from recurringActions.wordOfTheDayRecurringAction import \
    WordOfTheDayRecurringAction


class RecurringActionsJsonParser(RecurringActionsJsonParserInterface):

    def __init__(self, languagesRepository: LanguagesRepository):
        if not isinstance(languagesRepository, LanguagesRepository):
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')

        self.__languagesRepository: LanguagesRepository = languagesRepository

    async def parseSuperTrivia(
        self,
        enabled: bool,
        minutesBetween: Optional[int],
        jsonString: Optional[str],
        twitchChannel: str
    ) -> Optional[SuperTriviaRecurringAction]:
        if not utils.isValidStr(jsonString):
            return None

        return SuperTriviaRecurringAction(
            twitchChannel = twitchChannel,
            enabled = enabled,
            minutesBetween = minutesBetween
        )

    async def parseWeather(
        self,
        enabled: bool,
        minutesBetween: Optional[int],
        jsonString: Optional[str],
        twitchChannel: str
    ) -> Optional[WeatherRecurringAction]:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: Optional[Dict[str, Any]] = json.loads(jsonString)

        alertsOnly = utils.getBoolFromDict(
            d = jsonContents,
            key = 'alertsOnly',
            fallback = True
        )

        return WeatherRecurringAction(
            twitchChannel = twitchChannel,
            alertsOnly = alertsOnly,
            enabled = enabled,
            minutesBetween = minutesBetween
        )

    async def parseWordOfTheDay(
        self,
        enabled: bool,
        minutesBetween: Optional[int],
        jsonString: Optional[str],
        twitchChannel: str
    ) -> Optional[WordOfTheDayRecurringAction]:
        if not utils.isValidStr(jsonString):
            return None

        jsonContents: Optional[Dict[str, Any]] = json.loads(jsonString)

        wotdApiCode = utils.getStrFromDict(
            d = jsonContents,
            key = 'languageEntry',
            fallback = ''
        )

        if not utils.isValidStr(wotdApiCode):
            return None

        languageEntry = await self.__languagesRepository.requireLanguageForWotdApiCode(wotdApiCode)

        return WordOfTheDayRecurringAction(
            twitchChannel = twitchChannel,
            enabled = enabled,
            minutesBetween = minutesBetween,
            languageEntry = languageEntry
        )

    async def __superTriviaToJson(self, action: SuperTriviaRecurringAction) -> str:
        if not isinstance(action, SuperTriviaRecurringAction):
            raise ValueError(f'action argument is malformed: \"{action}\"')

        jsonContents: Dict[str, Any] = dict()

        return json.dumps(jsonContents)

    async def toJson(self, action: RecurringAction) -> str:
        if not isinstance(action, RecurringAction):
            raise ValueError(f'action argument is malformed: \"{action}\"')

        actionType = action.getActionType()

        if actionType is RecurringActionType.SUPER_TRIVIA:
            return await self.__superTriviaToJson(action)
        elif actionType is RecurringActionType.WEATHER:
            return await self.__weatherToJson(action)
        elif actionType is RecurringActionType.WORD_OF_THE_DAY:
            return await self.__wordOfTheDayToJson(action)
        else:
            raise RuntimeError(f'Encountered unknown actionType (\"{actionType}\") for action (\"{action}\")')

    async def __weatherToJson(self, action: WeatherRecurringAction) -> str:
        if not isinstance(action, WeatherRecurringAction):
            raise ValueError(f'action argument is malformed: \"{action}\"')

        jsonContents: Dict[str, Any] = {
            'alertsOnly': action.isAlertsOnly()
        }

        return json.dumps(jsonContents)

    async def __wordOfTheDayToJson(self, action: WordOfTheDayRecurringAction) -> str:
        if not isinstance(action, WordOfTheDayRecurringAction):
            raise ValueError(f'action argument is malformed: \"{action}\"')

        jsonContents: Dict[str, Any] = {
            'languageEntry': action.requireLanguageEntry().getWotdApiCode()
        }

        return json.dumps(jsonContents)
