import pytest

from src.trivia.misc.triviaDifficultyParser import TriviaDifficultyParser
from src.trivia.misc.triviaDifficultyParserInterface import TriviaDifficultyParserInterface
from src.trivia.triviaDifficulty import TriviaDifficulty


class TestTriviaDifficultyParser:

    parser: TriviaDifficultyParserInterface = TriviaDifficultyParser()

    @pytest.mark.asyncio
    async def test_parse_withEasy(self):
        result = await self.parser.parse('easy')
        assert result is TriviaDifficulty.EASY

    @pytest.mark.asyncio
    async def test_parse_withEmptyString(self):
        result: TriviaDifficulty | None = None

        with pytest.raises(ValueError):
            result = await self.parser.parse('')

        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withHard(self):
        result = await self.parser.parse('hard')
        assert result is TriviaDifficulty.HARD

    @pytest.mark.asyncio
    async def test_parse_withMedium(self):
        result = await self.parser.parse('medium')
        assert result is TriviaDifficulty.MEDIUM

    @pytest.mark.asyncio
    async def test_parse_withNone(self):
        result: TriviaDifficulty | None = None

        with pytest.raises(ValueError):
            result = await self.parser.parse(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withWhitespaceString(self):
        result: TriviaDifficulty | None = None

        with pytest.raises(ValueError):
            result = await self.parser.parse(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withNegative1(self):
        result = await self.parser.parse(-1)
        assert result is TriviaDifficulty.UNKNOWN

    @pytest.mark.asyncio
    async def test_parse_with0(self):
        result = await self.parser.parse(0)
        assert result is TriviaDifficulty.UNKNOWN

    @pytest.mark.asyncio
    async def test_parse_with1(self):
        result = await self.parser.parse(1)
        assert result is TriviaDifficulty.EASY

    @pytest.mark.asyncio
    async def test_parse_with2(self):
        result = await self.parser.parse(2)
        assert result is TriviaDifficulty.MEDIUM

    @pytest.mark.asyncio
    async def test_parse_with3(self):
        result = await self.parser.parse(3)
        assert result is TriviaDifficulty.HARD
