import pytest

from src.streamElements.models.streamElementsVoice import StreamElementsVoice
from src.streamElements.parser.streamElementsJsonParser import StreamElementsJsonParser
from src.streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from src.streamElements.parser.streamElementsMessageVoiceParser import \
    StreamElementsMessageVoiceParser
from src.streamElements.parser.streamElementsMessageVoiceParserInterface import \
    StreamElementsMessageVoiceParserInterface


class TestStreamElementsMessageVoiceParser:

    streamElementsJsonParser: StreamElementsJsonParserInterface = StreamElementsJsonParser()

    parser: StreamElementsMessageVoiceParserInterface = StreamElementsMessageVoiceParser(
        streamElementsJsonParser = streamElementsJsonParser
    )

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withAmyMessage(self):
        result = await self.parser.determineVoiceFromMessage('amy: Hello, World!')
        assert isinstance(result, StreamElementsMessageVoiceParserInterface.Result)
        assert result.message == 'Hello, World!'
        assert result.voice is StreamElementsVoice.AMY

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withBrianMessage(self):
        result = await self.parser.determineVoiceFromMessage('brian: Hello, World!')
        assert isinstance(result, StreamElementsMessageVoiceParserInterface.Result)
        assert result.message == 'Hello, World!'
        assert result.voice is StreamElementsVoice.BRIAN

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withEmptyString(self):
        result = await self.parser.determineVoiceFromMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withJoeyMessage(self):
        result = await self.parser.determineVoiceFromMessage('joey: Hello, World!')
        assert isinstance(result, StreamElementsMessageVoiceParserInterface.Result)
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

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, StreamElementsMessageVoiceParser)
        assert isinstance(self.parser, StreamElementsMessageVoiceParserInterface)
