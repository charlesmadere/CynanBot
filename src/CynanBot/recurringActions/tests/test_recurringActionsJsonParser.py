import json
from typing import Dict

import pytest

from CynanBot.language.languagesRepository import LanguagesRepository
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.recurringActions.recurringAction import RecurringAction
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
