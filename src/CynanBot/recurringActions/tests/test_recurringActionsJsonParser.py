import json
from typing import Any, Dict

import pytest

from CynanBot.language.languagesRepository import LanguagesRepository
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.recurringActions.recurringActionsJsonParser import \
    RecurringActionsJsonParser
from CynanBot.recurringActions.recurringActionsJsonParserInterface import \
    RecurringActionsJsonParserInterface
from CynanBot.recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from CynanBot.recurringActions.weatherRecurringAction import \
    WeatherRecurringAction
from CynanBot.recurringActions.wordOfTheDayRecurringAction import \
    WordOfTheDayRecurringAction
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestRecurringActionsJsonParser():

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

    timber: TimberInterface = TimberStub()

    parser: RecurringActionsJsonParserInterface = RecurringActionsJsonParser(
        languagesRepository = languagesRepository,
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseSuperTrivia1(self):
        action = await self.parser.parseSuperTrivia(
            enabled = True,
            minutesBetween = None,
            jsonString = '{}',
            twitchChannel = 'smCharles'
        )

        assert isinstance(action, SuperTriviaRecurringAction)
        assert action.getMinutesBetween() is None
        assert action.getTwitchChannel() == 'smCharles'
        assert action.isEnabled()

    @pytest.mark.asyncio
    async def test_parseSuperTrivia2(self):
        action = await self.parser.parseSuperTrivia(
            enabled = False,
            minutesBetween = 60,
            jsonString = '{}',
            twitchChannel = 'smCharles'
        )

        assert isinstance(action, SuperTriviaRecurringAction)
        assert action.getMinutesBetween() == 60
        assert action.getTwitchChannel() == 'smCharles'
        assert not action.isEnabled()

    @pytest.mark.asyncio
    async def test_parseSuperTrivia_withJsonStringEmpty(self):
        action = await self.parser.parseSuperTrivia(
            enabled = True,
            minutesBetween = None,
            jsonString = '',
            twitchChannel = 'smCharles'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseSuperTrivia_withJsonStringNone(self):
        action = await self.parser.parseSuperTrivia(
            enabled = True,
            minutesBetween = None,
            jsonString = None,
            twitchChannel = 'smCharles'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseWeather1(self):
        action = await self.parser.parseWeather(
            enabled = True,
            minutesBetween = None,
            jsonString = '{}',
            twitchChannel = 'smCharles'
        )

        assert isinstance(action, WeatherRecurringAction)
        assert action.getMinutesBetween() is None
        assert action.getTwitchChannel() == 'smCharles'
        assert action.isAlertsOnly()
        assert action.isEnabled()

    @pytest.mark.asyncio
    async def test_parseWeather2(self):
        jsonObject: Dict[str, Any] = {
            'alertsOnly': True
        }

        action = await self.parser.parseWeather(
            enabled = False,
            minutesBetween = 60,
            jsonString = json.dumps(jsonObject),
            twitchChannel = 'smCharles'
        )

        assert isinstance(action, WeatherRecurringAction)
        assert action.getMinutesBetween() == 60
        assert action.getTwitchChannel() == 'smCharles'
        assert action.isAlertsOnly()
        assert not action.isEnabled()

    @pytest.mark.asyncio
    async def test_parseWeather_withJsonStringEmpty(self):
        action = await self.parser.parseWeather(
            enabled = True,
            minutesBetween = None,
            jsonString = '',
            twitchChannel = 'smCharles'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseWeather_withJsonStringNone(self):
        action = await self.parser.parseWeather(
            enabled = True,
            minutesBetween = None,
            jsonString = None,
            twitchChannel = 'smCharles'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseWordOfTheDay_withJsonStringEmpty(self):
        action = await self.parser.parseWordOfTheDay(
            enabled = True,
            minutesBetween = None,
            jsonString = '',
            twitchChannel = 'smCharles'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseWordOfTheDay_withJsonStringNone(self):
        action = await self.parser.parseWordOfTheDay(
            enabled = True,
            minutesBetween = None,
            jsonString = None,
            twitchChannel = 'smCharles'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_toJson_withSuperTriviaAction(self):
        action = SuperTriviaRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles'
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, Dict)
        assert len(jsonObject) == 0

    @pytest.mark.asyncio
    async def test_toJson_withWeatherRecurringAction_alertsOnlyFalse(self):
        action = WeatherRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles',
            alertsOnly = False
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, Dict)
        assert len(jsonObject) == 1
        assert jsonObject.get('alertsOnly', None) is action.isAlertsOnly()

    @pytest.mark.asyncio
    async def test_toJson_withWeatherRecurringAction_alertsOnlyTrue(self):
        action = WeatherRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles',
            alertsOnly = True
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, Dict)
        assert len(jsonObject) == 1
        assert jsonObject.get('alertsOnly', None) is action.isAlertsOnly()

    @pytest.mark.asyncio
    async def test_toJson_withWordOfTheDayRecurringAction_languageEntryJapanese(self):
        languageEntry = await self.languagesRepository.requireLanguageForWotdApiCode('ja')

        action = WordOfTheDayRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles',
            languageEntry = languageEntry
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, Dict)
        assert len(jsonObject) == 1
        assert jsonObject.get('languageEntry', None) == languageEntry.getWotdApiCode()

    @pytest.mark.asyncio
    async def test_toJson_withWordOfTheDayRecurringAction_languageEntryNone(self):
        action = WordOfTheDayRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles'
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, Dict)
        assert len(jsonObject) == 0
