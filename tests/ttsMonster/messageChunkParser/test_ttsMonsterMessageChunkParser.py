import pytest
from frozenlist import FrozenList

from src.ttsMonster.messageChunkParser.ttsMonsterMessageChunkParser import TtsMonsterMessageChunkParser
from src.ttsMonster.messageChunkParser.ttsMonsterMessageChunkParserInterface import \
    TtsMonsterMessageChunkParserInterface
from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TestTtsMonsterMessageChunkParser:

    parser: TtsMonsterMessageChunkParserInterface = TtsMonsterMessageChunkParser()

    @pytest.mark.asyncio
    async def test_parse_withBasicMessage1(self):
        results = await self.parser.parse(
            message = 'Hello, World!',
            defaultVoice = TtsMonsterVoice.BRIAN
        )

        assert isinstance(results, FrozenList)
        assert len(results) == 1

        result = results[0]
        assert result.message == 'Hello, World!'
        assert result.voice is TtsMonsterVoice.BRIAN

    @pytest.mark.asyncio
    async def test_parse_withBasicMessage2(self):
        results = await self.parser.parse(
            message = 'shadow: Hello, World!',
            defaultVoice = TtsMonsterVoice.BRIAN
        )

        assert isinstance(results, FrozenList)
        assert len(results) == 1

        result = results[0]
        assert result.message == 'Hello, World!'
        assert result.voice is TtsMonsterVoice.SHADOW

    @pytest.mark.asyncio
    async def test_parse_withBasicMessage3(self):
        results = await self.parser.parse(
            message = 'SHADOW: Hello, World!',
            defaultVoice = TtsMonsterVoice.BRIAN
        )

        assert isinstance(results, FrozenList)
        assert len(results) == 1

        result = results[0]
        assert result.message == 'Hello, World!'
        assert result.voice is TtsMonsterVoice.SHADOW

    @pytest.mark.asyncio
    async def test_parse_withEmptyMessage(self):
        results = await self.parser.parse(
            message = '',
            defaultVoice = TtsMonsterVoice.BRIAN
        )

        assert results is None

    @pytest.mark.asyncio
    async def test_parse_withMissingVoiceChunks1(self):
        results = await self.parser.parse(
            message = 'Brian: Shadow: Hello, Brian: Witch: World! Shadow:',
            defaultVoice = TtsMonsterVoice.BRIAN
        )

        assert isinstance(results, FrozenList)
        assert len(results) == 2

        result = results[0]
        assert result.message == 'Hello,'
        assert result.voice is TtsMonsterVoice.SHADOW

        result = results[1]
        assert result.message == 'World!'
        assert result.voice is TtsMonsterVoice.WITCH

    @pytest.mark.asyncio
    async def test_parse_withMissingVoiceChunks2(self):
        results = await self.parser.parse(
            message = 'Brian: Shadow: Brian: Witch: Shadow: Jazz:',
            defaultVoice = TtsMonsterVoice.ZERO_TWO
        )

        assert results is None

    @pytest.mark.asyncio
    async def test_parse_withNoneMessage(self):
        results = await self.parser.parse(
            message = None,
            defaultVoice = TtsMonsterVoice.BRIAN
        )

        assert results is None

    @pytest.mark.asyncio
    async def test_parse_withWhitespaceMessage(self):
        results = await self.parser.parse(
            message = ' ',
            defaultVoice = TtsMonsterVoice.BRIAN
        )

        assert results is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, TtsMonsterMessageChunkParser)
        assert isinstance(self.parser, TtsMonsterMessageChunkParserInterface)
