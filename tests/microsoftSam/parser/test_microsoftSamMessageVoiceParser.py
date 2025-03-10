import pytest

from src.microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from src.microsoftSam.parser.microsoftSamJsonParser import MicrosoftSamJsonParser
from src.microsoftSam.parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from src.microsoftSam.parser.microsoftSamMessageVoiceParser import MicrosoftSamMessageVoiceParser
from src.microsoftSam.parser.microsoftSamMessageVoiceParserInterface import MicrosoftSamMessageVoiceParserInterface


class TestMicrosoftSamMessageVoiceParser:

    microsoftSamJsonParser: MicrosoftSamJsonParserInterface = MicrosoftSamJsonParser()

    parser: MicrosoftSamMessageVoiceParserInterface = MicrosoftSamMessageVoiceParser(
        microsoftSamJsonParser = microsoftSamJsonParser
    )

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withBonziBuddyMessage(self):
        result = await self.parser.determineVoiceFromMessage('bonzi_buddy: Hello, World!')
        assert isinstance(result, MicrosoftSamMessageVoiceParserInterface.Result)
        assert result.voice is MicrosoftSamVoice.BONZI_BUDDY
        assert result.message == 'Hello, World!'

        result = await self.parser.determineVoiceFromMessage('bonzibuddy: Hello, World!')
        assert isinstance(result, MicrosoftSamMessageVoiceParserInterface.Result)
        assert result.voice is MicrosoftSamVoice.BONZI_BUDDY
        assert result.message == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withEmptyString(self):
        result = await self.parser.determineVoiceFromMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withNone(self):
        result = await self.parser.determineVoiceFromMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withSamMessage(self):
        result = await self.parser.determineVoiceFromMessage('sam: Hello, World!')
        assert isinstance(result, MicrosoftSamMessageVoiceParserInterface.Result)
        assert result.voice is MicrosoftSamVoice.SAM
        assert result.message == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withWhitespaceString(self):
        result = await self.parser.determineVoiceFromMessage(' ')
        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, MicrosoftSamMessageVoiceParser)
        assert isinstance(self.parser, MicrosoftSamMessageVoiceParserInterface)
