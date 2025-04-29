import pytest

from src.trivia.misc.triviaQuestionTypeParser import TriviaQuestionTypeParser
from src.trivia.misc.triviaQuestionTypeParserInterface import TriviaQuestionTypeParserInterface
from src.trivia.questions.triviaQuestionType import TriviaQuestionType


class TestTriviaQuestionTypeParser:

    parser: TriviaQuestionTypeParserInterface = TriviaQuestionTypeParser()

    @pytest.mark.asyncio
    async def test_parse_withBoolString(self):
        result = await self.parser.parse('bool')
        assert result is TriviaQuestionType.TRUE_FALSE

    @pytest.mark.asyncio
    async def test_parse_withBooleanString(self):
        result = await self.parser.parse('boolean')
        assert result is TriviaQuestionType.TRUE_FALSE

    @pytest.mark.asyncio
    async def test_parse_withEmptyString(self):
        result: TriviaQuestionType | None = None

        with pytest.raises(TypeError):
            result = await self.parser.parse('')

        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withMultipleChoiceStrings(self):
        strings: set[str] = { 'multiple', 'multiple-choice', 'multiple_choice', 'multiple choice' }

        for string in strings:
            result = await self.parser.parse(string)
            assert result is TriviaQuestionType.MULTIPLE_CHOICE

    @pytest.mark.asyncio
    async def test_parse_withNone(self):
        result: TriviaQuestionType | None = None

        with pytest.raises(TypeError):
            result = await self.parser.parse(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withQuestionAnswerStrings(self):
        strings: set[str] = { 'question-answer', 'question_answer', 'question answer' }

        for string in strings:
            result = await self.parser.parse(string)
            assert result is TriviaQuestionType.QUESTION_ANSWER

    @pytest.mark.asyncio
    async def test_parse_withRandomNoise1(self):
        string = 'b44W5mrxgzHcLqgf'
        result: TriviaQuestionType | None = None

        with pytest.raises(ValueError):
            result = await self.parser.parse(string)

        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withRandomNoise2(self):
        string = 'PXZE0hfk0vFX6tBx'
        result: TriviaQuestionType | None = None

        with pytest.raises(ValueError):
            result = await self.parser.parse(string)

        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withTrueFalseStrings(self):
        strings: set[str] = { 'true-false', 'true_false', 'true false' }

        for string in strings:
            result = await self.parser.parse(string)
            assert result is TriviaQuestionType.TRUE_FALSE

    @pytest.mark.asyncio
    async def test_parse_withWhitespaceString(self):
        result: TriviaQuestionType | None = None

        with pytest.raises(TypeError):
            result = await self.parser.parse(' ')

        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, TriviaQuestionTypeParser)
        assert isinstance(self.parser, TriviaQuestionTypeParserInterface)

    @pytest.mark.asyncio
    async def test_serialize(self):
        results: set[str] = set()

        for triviaQuestionType in TriviaQuestionType:
            results.add(await self.parser.serialize(triviaQuestionType))

        assert len(results) == len(TriviaQuestionType)

    @pytest.mark.asyncio
    async def test_serialize_withMultipleChoice(self):
        result = await self.parser.serialize(TriviaQuestionType.MULTIPLE_CHOICE)
        assert result == 'multiple-choice'

    @pytest.mark.asyncio
    async def test_serialize_withQuestionAnswer(self):
        result = await self.parser.serialize(TriviaQuestionType.QUESTION_ANSWER)
        assert result == 'question-answer'

    @pytest.mark.asyncio
    async def test_serialize_withTrueFalse(self):
        result = await self.parser.serialize(TriviaQuestionType.TRUE_FALSE)
        assert result == 'true-false'
