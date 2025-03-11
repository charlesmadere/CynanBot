import pytest

from src.microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from src.microsoft.parser.microsoftTtsJsonParser import MicrosoftTtsJsonParser
from src.microsoft.parser.microsoftTtsJsonParserInterface import MicrosoftTtsJsonParserInterface


class TestMicrosoftTtsJsonParser:

    parser: MicrosoftTtsJsonParserInterface = MicrosoftTtsJsonParser()

    @pytest.mark.asyncio
    async def test_parseVoice_withDavid(self):
        result = await self.parser.parseVoice('david')
        assert result is MicrosoftTtsVoice.DAVID

    @pytest.mark.asyncio
    async def test_parseVoice_withEmptyString(self):
        result = await self.parser.parseVoice(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withHaruka(self):
        result = await self.parser.parseVoice('haruka')
        assert result is MicrosoftTtsVoice.HARUKA

    @pytest.mark.asyncio
    async def test_parseVoice_withHortense(self):
        result = await self.parser.parseVoice('hortense')
        assert result is MicrosoftTtsVoice.HORTENSE

    @pytest.mark.asyncio
    async def test_parseVoice_withNone(self):
        result = await self.parser.parseVoice(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withWhitespaceString(self):
        result = await self.parser.parseVoice(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withZira(self):
        result = await self.parser.parseVoice('zira')
        assert result is MicrosoftTtsVoice.ZIRA

    @pytest.mark.asyncio
    async def test_requireVoice_withHaruka(self):
        result = await self.parser.requireVoice('haruka')
        assert result is MicrosoftTtsVoice.HARUKA

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, MicrosoftTtsJsonParser)
        assert isinstance(self.parser, MicrosoftTtsJsonParserInterface)

    @pytest.mark.asyncio
    async def test_serializeVoice_withDavid(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.DAVID)
        assert result == 'david'

    @pytest.mark.asyncio
    async def test_serializeVoice_withHaruka(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.HARUKA)
        assert result == 'haruka'

    @pytest.mark.asyncio
    async def test_serializeVoice_withHortense(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.HORTENSE)
        assert result == 'hortense'

    @pytest.mark.asyncio
    async def test_serializeVoice_withZira(self):
        result = await self.parser.serializeVoice(MicrosoftTtsVoice.ZIRA)
        assert result == 'zira'
