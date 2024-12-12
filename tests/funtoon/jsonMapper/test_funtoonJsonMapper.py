import pytest

from src.funtoon.funtoonPkmnCatchType import FuntoonPkmnCatchType
from src.funtoon.jsonMapper.funtoonJsonMapper import FuntoonJsonMapper
from src.funtoon.jsonMapper.funtoonJsonMapperInterface import FuntoonJsonMapperInterface


class TestFuntoonJsonMapper:

    jsonMapper: FuntoonJsonMapperInterface = FuntoonJsonMapper()

    @pytest.mark.asyncio
    async def test_parseTriviaQuestion_withEmptyDictionary(self):
        result = await self.jsonMapper.parseTriviaQuestion(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTriviaQuestion_withNone(self):
        result = await self.jsonMapper.parseTriviaQuestion(None)
        assert result is None

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
