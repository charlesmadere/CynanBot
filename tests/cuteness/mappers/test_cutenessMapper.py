from datetime import datetime
from typing import Final

import pytest

from src.cuteness.mappers.cutenessMapper import CutenessMapper
from src.cuteness.mappers.cutenessMapperInterface import CutenessMapperInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestCutenessMapper:

    timber: Final[TimberInterface] = TimberStub()

    timeZoneRepository: Final[TimeZoneRepositoryInterface] = TimeZoneRepository()

    mapper: Final[CutenessMapperInterface] = CutenessMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository,
    )

    @pytest.mark.asyncio
    async def test_parseUtcYearAndMonthString_withEmptyString(self):
        result = await self.mapper.parseUtcYearAndMonthString('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUtcYearAndMonthString_withMalformedString1(self):
        result = await self.mapper.parseUtcYearAndMonthString('hello')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUtcYearAndMonthString_withMalformedString2(self):
        result = await self.mapper.parseUtcYearAndMonthString('qwerty')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUtcYearAndMonthString_withNone(self):
        result = await self.mapper.parseUtcYearAndMonthString(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUtcYearAndMonthString_withValidDate1(self):
        result = await self.mapper.parseUtcYearAndMonthString('2026-01')
        assert result is not None
        assert result.year == 2026
        assert result.month == 1
        assert result.tzinfo == self.timeZoneRepository.getDefault()

    @pytest.mark.asyncio
    async def test_parseUtcYearAndMonthString_withValidDate2(self):
        result = await self.mapper.parseUtcYearAndMonthString('2025-12')
        assert result is not None
        assert result.year == 2025
        assert result.month == 12
        assert result.tzinfo == self.timeZoneRepository.getDefault()

    @pytest.mark.asyncio
    async def test_parseUtcYearAndMonthString_withValidDate3(self):
        result = await self.mapper.parseUtcYearAndMonthString('1990-9')
        assert result is not None
        assert result.year == 1990
        assert result.month == 9
        assert result.tzinfo == self.timeZoneRepository.getDefault()

    @pytest.mark.asyncio
    async def test_parseUtcYearAndMonthString_withWhitespaceString(self):
        result = await self.mapper.parseUtcYearAndMonthString(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireUtcYearAndMonthString_withEmptyString(self):
        result: datetime | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireUtcYearAndMonthString('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireUtcYearAndMonthString_withMalformedString1(self):
        result: datetime | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireUtcYearAndMonthString('hello')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireUtcYearAndMonthString_withMalformedString2(self):
        result: datetime | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireUtcYearAndMonthString('qwerty')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireUtcYearAndMonthString_withNone(self):
        result: datetime | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireUtcYearAndMonthString(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireUtcYearAndMonthString_withValidDate1(self):
        result = await self.mapper.requireUtcYearAndMonthString('2020-3')
        assert result is not None
        assert result.year == 2020
        assert result.month == 3
        assert result.tzinfo == self.timeZoneRepository.getDefault()

    @pytest.mark.asyncio
    async def test_requireUtcYearAndMonthString_withValidDate2(self):
        result = await self.mapper.requireUtcYearAndMonthString('2022-08')
        assert result is not None
        assert result.year == 2022
        assert result.month == 8
        assert result.tzinfo == self.timeZoneRepository.getDefault()

    @pytest.mark.asyncio
    async def test_requireUtcYearAndMonthString_withWhitespaceString(self):
        result: datetime | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireUtcYearAndMonthString(' ')

        assert result is None

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, CutenessMapper)
        assert isinstance(self.mapper, CutenessMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeUtcYear_withDateTime1(self):
        value = datetime(
            year = 2018,
            month = 4,
            day = 16,
        )

        result = await self.mapper.serializeToUtcYearAndMonth(value)
        assert result == '2018-04'

    @pytest.mark.asyncio
    async def test_serializeUtcYear_withDateTime2(self):
        value = datetime(
            year = 2024,
            month = 1,
            day = 20,
        )

        result = await self.mapper.serializeToUtcYearAndMonth(value)
        assert result == '2024-01'

    @pytest.mark.asyncio
    async def test_serializeUtcYear_withDateTime3(self):
        value = datetime(
            year = 2023,
            month = 11,
            day = 30,
        )

        result = await self.mapper.serializeToUtcYearAndMonth(value)
        assert result == '2023-11'
