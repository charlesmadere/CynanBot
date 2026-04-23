from typing import Final

import pytest

from src.ecco.eccoConstants import EccoConstants
from src.ecco.eccoResponseParser import EccoResponseParser
from src.ecco.eccoResponseParserInterface import EccoResponseParserInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestEccoResponseParser:

    timber: Final[TimberInterface] = TimberStub()

    eccoConstants: Final[EccoConstants] = EccoConstants()

    parser: Final[EccoResponseParserInterface] = EccoResponseParser(
        eccoConstants = eccoConstants,
        timber = timber,
    )

    @pytest.mark.asyncio
    async def test_findTimerDateTimeValue(self):
        result = await self.parser.findTimerDateTimeValue('new Date("2026-07-21T12:00:00-08:00");')
        assert result is not None
        assert result.month == 7
        assert result.day == 21
        assert result.year == 2026
        assert result.hour == 12
        assert result.minute == 0
        assert result.second == 0

    @pytest.mark.asyncio
    async def test_findTimerDateTimeValue_withEmptyString(self):
        result = await self.parser.findTimerDateTimeValue('')
        assert result is None

    @pytest.mark.asyncio
    async def test_findTimerDateTimeValue_withNone(self):
        result = await self.parser.findTimerDateTimeValue(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_findTimerDateTimeValue_withWhitespaceString(self):
        result = await self.parser.findTimerDateTimeValue(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_findTimerScriptSource_withEmptyString(self):
        result = await self.parser.findTimerScriptSource('')
        assert result is None

    @pytest.mark.asyncio
    async def test_findTimerScriptSource_withNone(self):
        result = await self.parser.findTimerScriptSource(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_findTimerScriptSource_withWhitespaceString(self):
        result = await self.parser.findTimerScriptSource(' ')
        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, EccoResponseParser)
        assert isinstance(self.parser, EccoResponseParserInterface)
