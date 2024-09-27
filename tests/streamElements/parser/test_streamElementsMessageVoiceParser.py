import pytest

from src.streamElements.models.streamElementsVoice import StreamElementsVoice
from src.streamElements.parser.streamElementsMessageVoiceParser import StreamElementsMessageVoiceParser
from src.streamElements.parser.streamElementsMessageVoiceParserInterface import \
    StreamElementsMessageVoiceParserInterface


class TestStreamElementsMessageVoiceParser:

    parser: StreamElementsMessageVoiceParserInterface = StreamElementsMessageVoiceParser()

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withBrianMessage(self):
        result = await self.parser.determineVoiceFromMessage('brian: Hello, World!')
        assert result.message == 'Hello, World!'
        assert result.voice is StreamElementsVoice.BRIAN

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withEmptyString(self):
        result = await self.parser.determineVoiceFromMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withJoeyMessage(self):
        result = await self.parser.determineVoiceFromMessage('joey: Hello, World!')
        assert result.message == 'Hello, World!'
        assert result.voice is StreamElementsVoice.JOEY

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withNone(self):
        result = await self.parser.determineVoiceFromMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withSimpleMessage(self):
        result = await self.parser.determineVoiceFromMessage('Hello, World!')
        assert result is None

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withWhitespaceString(self):
        result = await self.parser.determineVoiceFromMessage(' ')
        assert result is None
