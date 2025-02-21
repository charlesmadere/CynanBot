import pytest

from src.halfLife.models.halfLifeVoice import HalfLifeVoice
from src.halfLife.parser.halfLifeVoiceParser import HalfLifeVoiceParser
from src.halfLife.parser.halfLifeMessageVoiceParser import HalfLifeMessageVoiceParser
from src.halfLife.parser.halfLifeMessageVoiceParserInterface import HalfLifeMessageVoiceParserInterface


class TestHalfLifeMessageVoiceParser:

    parser: HalfLifeMessageVoiceParserInterface = HalfLifeMessageVoiceParser(HalfLifeVoiceParser())

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withScientistMessage(self):
        result = await self.parser.determineVoiceFromMessage('scientist: Hello, World!')

        if result is None:
            assert False

        assert result.message == 'Hello, World!'
        assert result.voice is HalfLifeVoice.SCIENTIST

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withEmptyString(self):
        result = await self.parser.determineVoiceFromMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_determineVoiceFromMessage_withSoldierMessage(self):
        result = await self.parser.determineVoiceFromMessage('soldier: Hello, World!')
        if result is None:
            assert False

        assert result.message == 'Hello, World!'
        assert result.voice is HalfLifeVoice.SOLDIER

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
