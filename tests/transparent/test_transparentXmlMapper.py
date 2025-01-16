import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.transparent.transparentXmlMapper import TransparentXmlMapper
from src.transparent.transparentXmlMapperInterface import TransparentXmlMapperInterface


class TestTransparentXmlMapper:

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    xmlMapper: TransparentXmlMapperInterface = TransparentXmlMapper(
        timeZoneRepository = timeZoneRepository
    )

    @pytest.mark.asyncio
    async def test_parseTransparentResponse_withEmptyDictionary(self):
        result = await self.xmlMapper.parseTransparentResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTransparentResponse_withNone(self):
        result = await self.xmlMapper.parseTransparentResponse(None)
        assert result is None

    def test_sanity(self):
        assert self.xmlMapper is not None
        assert isinstance(self.xmlMapper, TransparentXmlMapperInterface)
        assert isinstance(self.xmlMapper, TransparentXmlMapper)
