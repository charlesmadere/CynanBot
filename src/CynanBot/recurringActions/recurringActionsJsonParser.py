import json
from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.recurringActionsJsonParserInterface import \
    RecurringActionsJsonParserInterface
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from CynanBot.recurringActions.weatherRecurringAction import \
    WeatherRecurringAction
from CynanBot.recurringActions.wordOfTheDayRecurringAction import \
    WordOfTheDayRecurringAction
from CynanBot.timber.timberInterface import TimberInterface


class RecurringActionsJsonParser(RecurringActionsJsonParserInterface):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface
    ):
        assert isinstance(languagesRepository, LanguagesRepositoryInterface), f"malformed {languagesRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__timber: TimberInterface = timber

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

        languageEntry: Optional[LanguageEntry] = None

        if utils.isValidStr(wotdApiCode):
            languageEntry = await self.__languagesRepository.getLanguageForWotdApiCode(
                wotdApiCode = wotdApiCode
            )

            if languageEntry is None:
                self.__timber.log('RecurringActionsJsonParser', f'Unable to find language for Word of the Day API code \"{wotdApiCode}\"')

        return WordOfTheDayRecurringAction(
            twitchChannel = twitchChannel,
            enabled = enabled,
            minutesBetween = minutesBetween,
            languageEntry = languageEntry
        )

    async def __superTriviaToJson(self, action: SuperTriviaRecurringAction) -> str:
        assert isinstance(action, SuperTriviaRecurringAction), f"malformed {action=}"

        jsonContents: Dict[str, Any] = dict()
        return json.dumps(jsonContents)

    async def toJson(self, action: RecurringAction) -> str:
        assert isinstance(action, RecurringAction), f"malformed {action=}"

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
        assert isinstance(action, WeatherRecurringAction), f"malformed {action=}"

        jsonContents: Dict[str, Any] = {
            'alertsOnly': action.isAlertsOnly()
        }

        return json.dumps(jsonContents)

    async def __wordOfTheDayToJson(self, action: WordOfTheDayRecurringAction) -> str:
        assert isinstance(action, WordOfTheDayRecurringAction), f"malformed {action=}"

        languageEntry = action.getLanguageEntry()
        wotdApiCode: Optional[str] = None

        if languageEntry is not None:
            wotdApiCode = languageEntry.getWotdApiCode()

        jsonContents: Dict[str, Any] = dict()

        if utils.isValidStr(wotdApiCode):
            jsonContents['languageEntry'] = wotdApiCode

        return json.dumps(jsonContents)
