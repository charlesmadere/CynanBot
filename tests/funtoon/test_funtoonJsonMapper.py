import pytest

from src.funtoon.funtoonJsonMapper import FuntoonJsonMapper
from src.funtoon.funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from src.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType


class TestFuntoonJsonMapper:

    jsonMapper: FuntoonJsonMapperInterface = FuntoonJsonMapper()

    @pytest.mark.asyncio
    async def test_serializePkmnCatchType_withGreat(self):
        result = await self.jsonMapper.serializePkmnCatchType(FuntoonPkmnCatchType.GREAT)
        assert result == 'great'

    @pytest.mark.asyncio
    async def test_serializePkmnCatchType_withNormal(self):
        result = await self.jsonMapper.serializePkmnCatchType(FuntoonPkmnCatchType.NORMAL)
        assert result == 'normal'

    @pytest.mark.asyncio
    async def test_serializePkmnCatchType_withUltra(self):
        result = await self.jsonMapper.serializePkmnCatchType(FuntoonPkmnCatchType.ULTRA)
        assert result == 'ultra'
