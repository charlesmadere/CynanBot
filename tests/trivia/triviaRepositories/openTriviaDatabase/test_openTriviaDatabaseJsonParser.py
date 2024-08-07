import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.trivia.misc.triviaDifficultyParser import TriviaDifficultyParser
from src.trivia.misc.triviaDifficultyParserInterface import TriviaDifficultyParserInterface
from src.trivia.misc.triviaQuestionTypeParser import TriviaQuestionTypeParser
from src.trivia.misc.triviaQuestionTypeParserInterface import TriviaQuestionTypeParserInterface
from src.trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseJsonParser import OpenTriviaDatabaseJsonParser
from src.trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseJsonParserInterface import \
    OpenTriviaDatabaseJsonParserInterface
from src.trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseResponseCode import \
    OpenTriviaDatabaseResponseCode


class TestOpenTriviaDatabaseJsonParser:

    timber: TimberInterface = TimberStub()

    triviaDifficultyParser: TriviaDifficultyParserInterface = TriviaDifficultyParser()

    triviaQuestionTypeParser: TriviaQuestionTypeParserInterface = TriviaQuestionTypeParser()

    parser: OpenTriviaDatabaseJsonParserInterface = OpenTriviaDatabaseJsonParser(
        timber = timber,
        triviaDifficultyParser = triviaDifficultyParser,
        triviaQuestionTypeParser = triviaQuestionTypeParser
    )

    @pytest.mark.asyncio
    async def test_parseQuestionsResponse_withEmptyDictionary(self):
        result = await self.parser.parseQuestionsResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseQuestionsResponse_withNone(self):
        result = await self.parser.parseQuestionsResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseResponseCode_withNone(self):
        result = await self.parser.parseResponseCode(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseResponseCode_withNegative1(self):
        result = await self.parser.parseResponseCode(-1)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseResponseCode_with0(self):
        result = await self.parser.parseResponseCode(0)
        assert result is OpenTriviaDatabaseResponseCode.SUCCESS

    @pytest.mark.asyncio
    async def test_parseResponseCode_with1(self):
        result = await self.parser.parseResponseCode(1)
        assert result is OpenTriviaDatabaseResponseCode.NO_RESULTS

    @pytest.mark.asyncio
    async def test_parseResponseCode_with2(self):
        result = await self.parser.parseResponseCode(2)
        assert result is OpenTriviaDatabaseResponseCode.INVALID_PARAMETER

    @pytest.mark.asyncio
    async def test_parseResponseCode_with3(self):
        result = await self.parser.parseResponseCode(3)
        assert result is OpenTriviaDatabaseResponseCode.TOKEN_NOT_FOUND

    @pytest.mark.asyncio
    async def test_parseResponseCode_with4(self):
        result = await self.parser.parseResponseCode(4)
        assert result is OpenTriviaDatabaseResponseCode.TOKEN_EMPTY

    @pytest.mark.asyncio
    async def test_parseResponseCode_with5(self):
        result = await self.parser.parseResponseCode(5)
        assert result is OpenTriviaDatabaseResponseCode.RATE_LIMIT

    @pytest.mark.asyncio
    async def test_parseResponseCode_with6(self):
        result = await self.parser.parseResponseCode(6)
        assert result is None

    @pytest.mark.asyncio
    async def test_requireResponseCode_withNegative1(self):
        result: OpenTriviaDatabaseResponseCode | None = None

        with pytest.raises(ValueError):
            result = await self.parser.requireResponseCode(-1)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireResponseCode_with0(self):
        result = await self.parser.requireResponseCode(0)
        assert result is OpenTriviaDatabaseResponseCode.SUCCESS

    @pytest.mark.asyncio
    async def test_requireResponseCode_with1(self):
        result = await self.parser.requireResponseCode(1)
        assert result is OpenTriviaDatabaseResponseCode.NO_RESULTS

    @pytest.mark.asyncio
    async def test_requireResponseCode_with2(self):
        result = await self.parser.requireResponseCode(2)
        assert result is OpenTriviaDatabaseResponseCode.INVALID_PARAMETER

    @pytest.mark.asyncio
    async def test_requireResponseCode_with3(self):
        result = await self.parser.requireResponseCode(3)
        assert result is OpenTriviaDatabaseResponseCode.TOKEN_NOT_FOUND

    @pytest.mark.asyncio
    async def test_requireResponseCode_with4(self):
        result = await self.parser.requireResponseCode(4)
        assert result is OpenTriviaDatabaseResponseCode.TOKEN_EMPTY

    @pytest.mark.asyncio
    async def test_requireResponseCode_with5(self):
        result = await self.parser.requireResponseCode(5)
        assert result is OpenTriviaDatabaseResponseCode.RATE_LIMIT

    @pytest.mark.asyncio
    async def test_requireResponseCode_with6(self):
        result: OpenTriviaDatabaseResponseCode | None = None

        with pytest.raises(ValueError):
            result = await self.parser.requireResponseCode(6)

        assert result is None
