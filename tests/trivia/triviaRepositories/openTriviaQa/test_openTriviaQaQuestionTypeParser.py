import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.trivia.triviaRepositories.openTriviaQa.exceptions import UnknownOpenTriviaQaQuestionTypeException
from src.trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionType import OpenTriviaQaQuestionType
from src.trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionTypeParser import OpenTriviaQaQuestionTypeParser
from src.trivia.triviaRepositories.openTriviaQa.openTriviaQaQuestionTypeParserInterface import \
    OpenTriviaQaQuestionTypeParserInterface


class TestOpenTriviaQaQuestionTypeParser:

    timber: TimberInterface = TimberStub()

    parser: OpenTriviaQaQuestionTypeParserInterface = OpenTriviaQaQuestionTypeParser(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parse_withEmptyString(self):
        result = await self.parser.parse('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withMultipleChoice(self):
        result = await self.parser.parse('multiple-choice')
        assert result is OpenTriviaQaQuestionType.MULTIPLE_CHOICE

    @pytest.mark.asyncio
    async def test_parse_withNone(self):
        result = await self.parser.parse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withTrueFalse(self):
        result = await self.parser.parse('true-false')
        assert result is OpenTriviaQaQuestionType.BOOLEAN

    @pytest.mark.asyncio
    async def test_parse_withWhitespaceString(self):
        result = await self.parser.parse(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_require_withEmptyString(self):
        result: OpenTriviaQaQuestionType | None = None

        with pytest.raises(UnknownOpenTriviaQaQuestionTypeException):
            result = await self.parser.require('')

        assert result is None

    @pytest.mark.asyncio
    async def test_require_withMultipleChoice(self):
        result = await self.parser.require('multiple-choice')
        assert result is OpenTriviaQaQuestionType.MULTIPLE_CHOICE

    @pytest.mark.asyncio
    async def test_require_withNone(self):
        result: OpenTriviaQaQuestionType | None = None

        with pytest.raises(UnknownOpenTriviaQaQuestionTypeException):
            result = await self.parser.require(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_require_withTrueFalse(self):
        result = await self.parser.require('true-false')
        assert result is OpenTriviaQaQuestionType.BOOLEAN

    @pytest.mark.asyncio
    async def test_require_withWhitespaceString(self):
        result: OpenTriviaQaQuestionType | None = None

        with pytest.raises(UnknownOpenTriviaQaQuestionTypeException):
            result = await self.parser.require(' ')

        assert result is None
