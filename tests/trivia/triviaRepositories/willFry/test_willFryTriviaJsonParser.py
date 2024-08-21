import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.trivia.misc.triviaDifficultyParser import TriviaDifficultyParser
from src.trivia.misc.triviaDifficultyParserInterface import TriviaDifficultyParserInterface
from src.trivia.triviaRepositories.willFry.willFryTriviaJsonParser import WillFryTriviaJsonParser
from src.trivia.triviaRepositories.willFry.willFryTriviaJsonParserInterface import WillFryTriviaJsonParserInterface
from src.trivia.triviaRepositories.willFry.willFryTriviaQuestionType import WillFryTriviaQuestionType


class TestWillFryTriviaJsonParser:

    timber: TimberInterface = TimberStub()

    triviaDifficultyParser: TriviaDifficultyParserInterface = TriviaDifficultyParser()

    jsonParser: WillFryTriviaJsonParserInterface = WillFryTriviaJsonParser(
        timber = timber,
        triviaDifficultyParser = triviaDifficultyParser
    )

    @pytest.mark.asyncio
    async def test_parseQuestionType_withEmptyString(self):
        result = await self.jsonParser.parseQuestionType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseQuestionType_withNone(self):
        result = await self.jsonParser.parseQuestionType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseQuestionType_withTextChoice(self):
        result = await self.jsonParser.parseQuestionType('text_choice')
        assert result is WillFryTriviaQuestionType.TEXT_CHOICE

    @pytest.mark.asyncio
    async def test_parseQuestionType_withWhitespaceString(self):
        result = await self.jsonParser.parseQuestionType(' ')
        assert result is None
