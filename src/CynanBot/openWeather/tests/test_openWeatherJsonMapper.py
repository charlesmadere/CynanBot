import pytest

from CynanBot.location.timeZoneRepository import TimeZoneRepository
from CynanBot.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from CynanBot.openWeather.openWeatherJsonMapper import OpenWeatherJsonMapper
from CynanBot.openWeather.openWeatherJsonMapperInterface import OpenWeatherJsonMapperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestOpenWeatherJsonMapper():

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    jsonMapper: OpenWeatherJsonMapperInterface = OpenWeatherJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    @pytest.mark.asyncio
    async def test_parseAirPollutionIndex_withNone(self):
        result = await self.jsonMapper.parseAirPollutionIndex(None)
        assert result is None

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
        assert isinstance(self.jsonMapper, OpenWeatherJsonMapperInterface)
