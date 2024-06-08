import pytest

from CynanBot.jisho.jishoJlptLevel import JishoJlptLevel
from CynanBot.jisho.jishoJsonMapper import JishoJsonMapper
from CynanBot.jisho.jishoJsonMapperInterface import JishoJsonMapperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestJishoJsonMapper():

    timber: TimberInterface = TimberStub()

    jsonMapper: JishoJsonMapperInterface = JishoJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseData_withEmptyDictionary(self):
        result = await self.jsonMapper.parseData(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseData_withNone(self):
        result = await self.jsonMapper.parseData(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseJlptLevel_withEmptyString(self):
        result = await self.jsonMapper.parseJlptLevel('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseJlptLevel_withJlptN1String(self):
        result = await self.jsonMapper.parseJlptLevel('jlpt-n1')
        assert result is JishoJlptLevel.N1

    @pytest.mark.asyncio
    async def test_parseJlptLevel_withJlptN2String(self):
        result = await self.jsonMapper.parseJlptLevel('jlpt-n2')
        assert result is JishoJlptLevel.N2

    @pytest.mark.asyncio
    async def test_parseJlptLevel_withJlptN3String(self):
        result = await self.jsonMapper.parseJlptLevel('jlpt-n3')
        assert result is JishoJlptLevel.N3

    @pytest.mark.asyncio
    async def test_parseJlptLevel_withJlptN4String(self):
        result = await self.jsonMapper.parseJlptLevel('jlpt-n4')
        assert result is JishoJlptLevel.N4

    @pytest.mark.asyncio
    async def test_parseJlptLevel_withJlptN5String(self):
        result = await self.jsonMapper.parseJlptLevel('jlpt-n5')
        assert result is JishoJlptLevel.N5

    @pytest.mark.asyncio
    async def test_parseJlptLevel_withNone(self):
        result = await self.jsonMapper.parseJlptLevel(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseJlptLevel_withWhitespaceString(self):
        result = await self.jsonMapper.parseJlptLevel(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseMeta_withEmptyDictionary(self):
        result = await self.jsonMapper.parseMeta(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseMeta_withNone(self):
        result = await self.jsonMapper.parseMeta(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseResponse_withNone(self):
        result = await self.jsonMapper.parseResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseResponse_withEmptyDictionary(self):
        result = await self.jsonMapper.parseResponse(dict())
        assert result is None

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, JishoJsonMapper)
        assert isinstance(self.jsonMapper, JishoJsonMapperInterface)
