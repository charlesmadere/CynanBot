import json
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.recurringActionsJsonParserInterface import \
    RecurringActionsJsonParserInterface
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
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__timber: TimberInterface = timber

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
            languageEntry = await self.__languagesRepository.getLanguageForWotdApiCode(
                wotdApiCode = wotdApiCode
            )

            if languageEntry is None:
                self.__timber.log('RecurringActionsJsonParser', f'Unable to find language for Word of the Day API code \"{wotdApiCode}\"')

        return WordOfTheDayRecurringAction(
            enabled = enabled,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            minutesBetween = minutesBetween,
            languageEntry = languageEntry
        )

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
            raise RuntimeError(f'Encountered unknown action type (\"{type(action)=}\") for action (\"{action}\")')

    async def __weatherToJson(self, action: WeatherRecurringAction) -> str:
        if not isinstance(action, WeatherRecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        jsonContents: dict[str, Any] = {
            'alertsOnly': action.isAlertsOnly()
        }

        return json.dumps(jsonContents)

    async def __wordOfTheDayToJson(self, action: WordOfTheDayRecurringAction) -> str:
        if not isinstance(action, WordOfTheDayRecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        languageEntry = action.getLanguageEntry()

        jsonContents: dict[str, Any] = dict()

        if languageEntry is not None and utils.isValidStr(languageEntry.wotdApiCode):
            jsonContents['languageEntry'] = languageEntry.wotdApiCode

        return json.dumps(jsonContents)
