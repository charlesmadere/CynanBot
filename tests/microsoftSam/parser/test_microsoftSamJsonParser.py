import pytest

from src.microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from src.microsoftSam.parser.microsoftSamJsonParser import MicrosoftSamJsonParser
from src.microsoftSam.parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface


class TestMicrosoftSamJsonParser:

    parser: MicrosoftSamJsonParserInterface = MicrosoftSamJsonParser()

    @pytest.mark.asyncio
    async def test_parseVoice_withBonziBuddy(self):
        result = await self.parser.parseVoice('bonzi_buddy')
        assert result is MicrosoftSamVoice.BONZI_BUDDY

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, MicrosoftSamJsonParser)
        assert isinstance(self.parser, MicrosoftSamJsonParserInterface)

    @pytest.mark.asyncio
    async def test_serializeVoice_withBonziBuddy(self):
        result = await self.parser.serializeVoice(MicrosoftSamVoice.BONZI_BUDDY)
        assert result == 'bonzi_buddy'
