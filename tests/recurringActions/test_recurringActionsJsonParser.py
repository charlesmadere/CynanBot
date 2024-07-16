import json
from typing import Any

import pytest

from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.recurringActions.cutenessRecurringAction import CutenessRecurringAction
from src.recurringActions.recurringActionType import RecurringActionType
from src.recurringActions.recurringActionsJsonParser import RecurringActionsJsonParser
from src.recurringActions.recurringActionsJsonParserInterface import RecurringActionsJsonParserInterface
from src.recurringActions.superTriviaRecurringAction import SuperTriviaRecurringAction
from src.recurringActions.weatherRecurringAction import WeatherRecurringAction
from src.recurringActions.wordOfTheDayRecurringAction import WordOfTheDayRecurringAction
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestRecurringActionsJsonParser:

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

    timber: TimberInterface = TimberStub()

    parser: RecurringActionsJsonParserInterface = RecurringActionsJsonParser(
        languagesRepository = languagesRepository,
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseActionType_withCuteness(self):
        result = await self.parser.parseActionType('cuteness')
        assert result is RecurringActionType.CUTENESS

    @pytest.mark.asyncio
    async def test_parseActionType_withEmptyString(self):
        result = await self.parser.parseActionType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseActionType_withNone(self):
        result = await self.parser.parseActionType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseActionType_withSuperTrivia(self):
        result = await self.parser.parseActionType('super_trivia')
        assert result is RecurringActionType.SUPER_TRIVIA

    @pytest.mark.asyncio
    async def test_parseActionType_withWeather(self):
        result = await self.parser.parseActionType('weather')
        assert result is RecurringActionType.WEATHER

    @pytest.mark.asyncio
    async def test_parseActionType_withWhitespaceString(self):
        result = await self.parser.parseActionType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseActionType_withWordOfTheDay(self):
        result = await self.parser.parseActionType('word_of_the_day')
        assert result is RecurringActionType.WORD_OF_THE_DAY

    @pytest.mark.asyncio
    async def test_parseCuteness1(self):
        action = await self.parser.parseCuteness(
            enabled = True,
            minutesBetween = None,
            jsonString = '{}',
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert isinstance(action, CutenessRecurringAction)
        assert action.isEnabled
        assert action.minutesBetween is None
        assert action.twitchChannel == 'smCharles'
        assert action.twitchChannelId == 'c'

    @pytest.mark.asyncio
    async def test_parseCuteness2(self):
        action = await self.parser.parseCuteness(
            enabled = False,
            minutesBetween = None,
            jsonString = '{}',
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert isinstance(action, CutenessRecurringAction)
        assert not action.isEnabled
        assert action.minutesBetween is None
        assert action.twitchChannel == 'smCharles'
        assert action.twitchChannelId == 'c'

    @pytest.mark.asyncio
    async def test_parseCuteness3(self):
        action = await self.parser.parseCuteness(
            enabled = True,
            minutesBetween = None,
            jsonString = None,
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseSuperTrivia1(self):
        action = await self.parser.parseSuperTrivia(
            enabled = True,
            minutesBetween = None,
            jsonString = '{}',
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert isinstance(action, SuperTriviaRecurringAction)
        assert action.isEnabled
        assert action.minutesBetween is None
        assert action.twitchChannel == 'smCharles'
        assert action.twitchChannelId == 'c'

    @pytest.mark.asyncio
    async def test_parseSuperTrivia2(self):
        action = await self.parser.parseSuperTrivia(
            enabled = False,
            minutesBetween = 60,
            jsonString = '{}',
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert isinstance(action, SuperTriviaRecurringAction)
        assert not action.isEnabled
        assert action.minutesBetween == 60
        assert action.twitchChannel == 'smCharles'
        assert action.twitchChannelId == 'c'

    @pytest.mark.asyncio
    async def test_parseSuperTrivia_withJsonStringEmpty(self):
        action = await self.parser.parseSuperTrivia(
            enabled = True,
            minutesBetween = None,
            jsonString = '',
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseSuperTrivia_withJsonStringNone(self):
        action = await self.parser.parseSuperTrivia(
            enabled = True,
            minutesBetween = None,
            jsonString = None,
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseWeather1(self):
        action = await self.parser.parseWeather(
            enabled = True,
            minutesBetween = None,
            jsonString = '{}',
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert isinstance(action, WeatherRecurringAction)
        assert action.isAlertsOnly
        assert action.isEnabled
        assert action.minutesBetween is None
        assert action.twitchChannel == 'smCharles'
        assert action.twitchChannelId == 'c'

    @pytest.mark.asyncio
    async def test_parseWeather2(self):
        jsonObject: dict[str, Any] = {
            'alertsOnly': True
        }

        action = await self.parser.parseWeather(
            enabled = False,
            minutesBetween = 60,
            jsonString = json.dumps(jsonObject),
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert isinstance(action, WeatherRecurringAction)
        assert action.isAlertsOnly
        assert not action.isEnabled
        assert action.minutesBetween == 60
        assert action.twitchChannel == 'smCharles'
        assert action.twitchChannelId == 'c'

    @pytest.mark.asyncio
    async def test_parseWeather3(self):
        jsonObject: dict[str, Any] = {
            'alertsOnly': False
        }

        action = await self.parser.parseWeather(
            enabled = True,
            minutesBetween = 120,
            jsonString = json.dumps(jsonObject),
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert isinstance(action, WeatherRecurringAction)
        assert not action.isAlertsOnly
        assert action.isEnabled
        assert action.minutesBetween == 120
        assert action.twitchChannel == 'smCharles'
        assert action.twitchChannelId == 'c'

    @pytest.mark.asyncio
    async def test_parseWeather_withJsonStringEmpty(self):
        action = await self.parser.parseWeather(
            enabled = True,
            minutesBetween = None,
            jsonString = '',
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseWeather_withJsonStringNone(self):
        action = await self.parser.parseWeather(
            enabled = True,
            minutesBetween = None,
            jsonString = None,
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseWordOfTheDay1(self):
        action = await self.parser.parseWordOfTheDay(
            enabled = True,
            minutesBetween = None,
            jsonString = '{}',
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert isinstance(action, WordOfTheDayRecurringAction)
        assert action.isEnabled
        assert action.languageEntry is None
        assert action.minutesBetween is None
        assert action.twitchChannel == 'smCharles'
        assert action.twitchChannelId == 'c'

        with pytest.raises(RuntimeError):
            action.requireLanguageEntry()

    @pytest.mark.asyncio
    async def test_parseWordOfTheDay2(self):
        jsonObject: dict[str, Any] = {
            'languageEntry': 'ja'
        }

        action = await self.parser.parseWordOfTheDay(
            enabled = False,
            minutesBetween = 180,
            jsonString = json.dumps(jsonObject),
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert isinstance(action, WordOfTheDayRecurringAction)
        assert not action.isEnabled
        assert action.minutesBetween == 180
        assert action.twitchChannel == 'smCharles'
        assert action.twitchChannelId == 'c'

        languageEntry = action.languageEntry
        assert languageEntry is not None
        assert languageEntry.wotdApiCode == 'ja'

        requiredLanguageEntry = action.requireLanguageEntry()
        assert languageEntry is requiredLanguageEntry

    @pytest.mark.asyncio
    async def test_parseWordOfTheDay_withJsonStringEmpty(self):
        action = await self.parser.parseWordOfTheDay(
            enabled = True,
            minutesBetween = None,
            jsonString = '',
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_parseWordOfTheDay_withJsonStringNone(self):
        action = await self.parser.parseWordOfTheDay(
            enabled = True,
            minutesBetween = None,
            jsonString = None,
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        assert action is None

    @pytest.mark.asyncio
    async def test_requireActionType_withCuteness(self):
        result = await self.parser.requireActionType('cuteness')
        assert result is RecurringActionType.CUTENESS

    @pytest.mark.asyncio
    async def test_requireActionType_withEmptyString(self):
        result: RecurringActionType | None = None

        with pytest.raises(ValueError):
            result = await self.parser.requireActionType('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireActionType_withSuperTrivia(self):
        result = await self.parser.requireActionType('super_trivia')
        assert result is RecurringActionType.SUPER_TRIVIA

    @pytest.mark.asyncio
    async def test_requireActionType_withWeather(self):
        result = await self.parser.requireActionType('weather')
        assert result is RecurringActionType.WEATHER

    @pytest.mark.asyncio
    async def test_requireActionType_withWhitespaceString(self):
        result: RecurringActionType | None = None

        with pytest.raises(ValueError):
            result = await self.parser.requireActionType(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireActionType_withWordOfTheDay(self):
        result = await self.parser.requireActionType('word_of_the_day')
        assert result is RecurringActionType.WORD_OF_THE_DAY

    @pytest.mark.asyncio
    async def test_serializeActionType_withCuteness(self):
        result = await self.parser.serializeActionType(RecurringActionType.CUTENESS)
        assert result == 'cuteness'

    @pytest.mark.asyncio
    async def test_serializeActionType_withSuperTrivia(self):
        result = await self.parser.serializeActionType(RecurringActionType.SUPER_TRIVIA)
        assert result == 'super_trivia'

    @pytest.mark.asyncio
    async def test_serializeActionType_withWeather(self):
        result = await self.parser.serializeActionType(RecurringActionType.WEATHER)
        assert result == 'weather'

    @pytest.mark.asyncio
    async def test_serializeActionType_withWordOfTheDay(self):
        result = await self.parser.serializeActionType(RecurringActionType.WORD_OF_THE_DAY)
        assert result == 'word_of_the_day'

    @pytest.mark.asyncio
    async def test_toJson_withSuperTriviaAction(self):
        action = SuperTriviaRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, dict)
        assert len(jsonObject) == 0

    @pytest.mark.asyncio
    async def test_toJson_withWeatherRecurringAction_alertsOnlyFalse(self):
        action = WeatherRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles',
            twitchChannelId = 'c',
            alertsOnly = False
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, dict)
        assert len(jsonObject) == 1
        assert jsonObject.get('alertsOnly') is action.isAlertsOnly

    @pytest.mark.asyncio
    async def test_toJson_withWeatherRecurringAction_alertsOnlyTrue(self):
        action = WeatherRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles',
            twitchChannelId = 'c',
            alertsOnly = True
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, dict)
        assert len(jsonObject) == 1
        assert jsonObject.get('alertsOnly') is action.isAlertsOnly

    @pytest.mark.asyncio
    async def test_toJson_withWordOfTheDayRecurringAction_languageEntryJapanese(self):
        languageEntry = await self.languagesRepository.requireLanguageForWotdApiCode('ja')

        action = WordOfTheDayRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles',
            twitchChannelId = 'c',
            languageEntry = languageEntry
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, dict)
        assert len(jsonObject) == 1
        assert jsonObject.get('languageEntry') == languageEntry.wotdApiCode

    @pytest.mark.asyncio
    async def test_toJson_withWordOfTheDayRecurringAction_languageEntryNone(self):
        action = WordOfTheDayRecurringAction(
            enabled = True,
            twitchChannel = 'smCharles',
            twitchChannelId = 'c'
        )

        jsonString = await self.parser.toJson(action)
        assert isinstance(jsonString, str)
        assert len(jsonString) != 0
        assert not jsonString.isspace()

        jsonObject = json.loads(jsonString)
        assert isinstance(jsonObject, dict)
        assert len(jsonObject) == 0

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, RecurringActionsJsonParserInterface)
        assert isinstance(self.parser, RecurringActionsJsonParser)
