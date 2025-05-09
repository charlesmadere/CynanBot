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
    async def test_findTimerDateTimeValue_withNone(self):
        result = await self.parser.findTimerDateTimeValue(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_findTimerScriptSource_withNone(self):
        result = await self.parser.findTimerScriptSource(None)
        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, EccoResponseParser)
        assert isinstance(self.parser, EccoResponseParserInterface)
