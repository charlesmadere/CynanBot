import pytest

from src.ecco.eccoResponseParser import EccoResponseParser
from src.ecco.eccoResponseParserInterface import EccoResponseParserInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestEccoResponseParser:

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    parser: EccoResponseParserInterface = EccoResponseParser(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    @pytest.mark.asyncio
    async def test_findTimerDateTimeValue_withNoTimeZone(self):
        timeZone = self.timeZoneRepository.getDefault()
        result = await self.parser.findTimerDateTimeValue('new Date(\"Apr 22, 2026 13:00:00\")')
        assert result is not None
        assert result.month == 4
        assert result.day == 22
        assert result.year == 2026
        assert result.hour == 13
        assert result.minute == 0
        assert result.second == 0
        assert result.tzinfo is timeZone

    @pytest.mark.asyncio
    async def test_findTimerDateTimeValue_withTimeZone(self):
        timeZone = self.timeZoneRepository.getTimeZone('America/New_York')
        result = await self.parser.findTimerDateTimeValue('new Date(\"Apr 22, 2026 13:00:00 EST\")')
        assert result is not None
        assert result.month == 4
        assert result.day == 22
        assert result.year == 2026
        assert result.hour == 13
        assert result.minute == 0
        assert result.second == 0
        assert result.tzinfo is timeZone

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
