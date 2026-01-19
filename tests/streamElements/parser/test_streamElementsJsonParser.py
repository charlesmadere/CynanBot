import pytest

from src.streamElements.models.streamElementsVoice import StreamElementsVoice
from src.streamElements.parser.streamElementsJsonParser import StreamElementsJsonParser
from src.streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface


class TestStreamElementsJsonParser:

    parser: StreamElementsJsonParserInterface = StreamElementsJsonParser()

    @pytest.mark.asyncio
    async def test_parseVoice_withAmy(self):
        result = await self.parser.parseVoice('amy')
        assert result is StreamElementsVoice.AMY

    @pytest.mark.asyncio
    async def test_parseVoice_withBrian(self):
        result = await self.parser.parseVoice('brian')
        assert result is StreamElementsVoice.BRIAN

    @pytest.mark.asyncio
    async def test_parseVoice_withEmma(self):
        result = await self.parser.parseVoice('emma')
        assert result is StreamElementsVoice.EMMA

    @pytest.mark.asyncio
    async def test_parseVoice_withEmptyString(self):
        result = await self.parser.parseVoice('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withJoey(self):
        result = await self.parser.parseVoice('joey')
        assert result is StreamElementsVoice.JOEY

    @pytest.mark.asyncio
    async def test_parseVoice_withNone(self):
        result = await self.parser.parseVoice(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withWhitespaceString(self):
        result = await self.parser.parseVoice(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoice_withAmy(self):
        result = await self.parser.requireVoice('amy')
        assert result is StreamElementsVoice.AMY

    @pytest.mark.asyncio
    async def test_requireVoice_withBrian(self):
        result = await self.parser.requireVoice('brian')
        assert result is StreamElementsVoice.BRIAN

    @pytest.mark.asyncio
    async def test_requireVoice_withEmma(self):
        result = await self.parser.requireVoice('emma')
        assert result is StreamElementsVoice.EMMA

    @pytest.mark.asyncio
    async def test_requireVoice_withEmptyString(self):
        result: StreamElementsVoice | None = None

        with pytest.raises(ValueError):
            result = await self.parser.requireVoice('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoice_withJoey(self):
        result = await self.parser.requireVoice('joey')
        assert result is StreamElementsVoice.JOEY

    @pytest.mark.asyncio
    async def test_requireVoice_withNone(self):
        result: StreamElementsVoice | None = None

        with pytest.raises(ValueError):
            result = await self.parser.requireVoice(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoice_withWhitespaceString(self):
        result: StreamElementsVoice | None = None

        with pytest.raises(ValueError):
            result = await self.parser.requireVoice(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_serializeVoice(self):
        results: set[str] = set()

        for voice in StreamElementsVoice:
            results.add(await self.parser.serializeVoice(voice))

        assert len(results) == len(StreamElementsVoice)

    @pytest.mark.asyncio
    async def test_serializeVoice_withAmy(self):
        result = await self.parser.serializeVoice(StreamElementsVoice.AMY)
        assert result == 'amy'

    @pytest.mark.asyncio
    async def test_serializeVoice_withBrian(self):
        result = await self.parser.serializeVoice(StreamElementsVoice.BRIAN)
        assert result == 'brian'

    @pytest.mark.asyncio
    async def test_serializeVoice_withEmma(self):
        result = await self.parser.serializeVoice(StreamElementsVoice.EMMA)
        assert result == 'emma'

    @pytest.mark.asyncio
    async def test_serializeVoice_withJoey(self):
        result = await self.parser.serializeVoice(StreamElementsVoice.JOEY)
        assert result == 'joey'
