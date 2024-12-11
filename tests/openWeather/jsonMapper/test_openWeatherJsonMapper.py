import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.openWeather.jsonMapper.openWeatherJsonMapper import OpenWeatherJsonMapper
from src.openWeather.jsonMapper.openWeatherJsonMapperInterface import OpenWeatherJsonMapperInterface
from src.openWeather.openWeatherAirPollutionIndex import OpenWeatherAirPollutionIndex
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestOpenWeatherJsonMapper:

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    jsonMapper: OpenWeatherJsonMapperInterface = OpenWeatherJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    @pytest.mark.asyncio
    async def test_parseAirPollutionIndex_withFive(self):
        result = await self.jsonMapper.parseAirPollutionIndex(5)
        assert result is OpenWeatherAirPollutionIndex.VERY_POOR

    @pytest.mark.asyncio
    async def test_parseAirPollutionIndex_withFour(self):
        result = await self.jsonMapper.parseAirPollutionIndex(4)
        assert result is OpenWeatherAirPollutionIndex.POOR

    @pytest.mark.asyncio
    async def test_parseAirPollutionIndex_withNone(self):
        result = await self.jsonMapper.parseAirPollutionIndex(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseAirPollutionIndex_withOne(self):
        result = await self.jsonMapper.parseAirPollutionIndex(1)
        assert result is OpenWeatherAirPollutionIndex.GOOD

    @pytest.mark.asyncio
    async def test_parseAirPollutionIndex_withThree(self):
        result = await self.jsonMapper.parseAirPollutionIndex(3)
        assert result is OpenWeatherAirPollutionIndex.MODERATE

    @pytest.mark.asyncio
    async def test_parseAirPollutionIndex_withTwo(self):
        result = await self.jsonMapper.parseAirPollutionIndex(2)
        assert result is OpenWeatherAirPollutionIndex.FAIR

    @pytest.mark.asyncio
    async def test_parseAirPollutionIndex_withZero(self):
        result = await self.jsonMapper.parseAirPollutionIndex(0)
        assert result is OpenWeatherAirPollutionIndex.GOOD

    @pytest.mark.asyncio
    async def test_parseAirPollutionReport_withNone(self):
        result = await self.jsonMapper.parseAirPollutionReport(
            jsonContents = None,
            timeZone = self.timeZoneRepository.getDefault()
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_parseAlert_withNone(self):
        result = await self.jsonMapper.parseAlert(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseDay_withNone(self):
        result = await self.jsonMapper.parseDay(
            jsonContents = None,
            timeZone = self.timeZoneRepository.getDefault()
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_parseFeelsLike_withNone(self):
        result = await self.jsonMapper.parseFeelsLike(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseMoment_withNone(self):
        result = await self.jsonMapper.parseMoment(
            jsonContents = None,
            timeZone = self.timeZoneRepository.getDefault()
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_parseMomentDescription_withNone(self):
        result = await self.jsonMapper.parseMomentDescription(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTemperature_withNone(self):
        result = await self.jsonMapper.parseTemperature(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWeatherReport_withNone(self):
        result = await self.jsonMapper.parseWeatherReport(None)
        assert result is None

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, OpenWeatherJsonMapper)
        assert isinstance(self.jsonMapper, OpenWeatherJsonMapperInterface)
