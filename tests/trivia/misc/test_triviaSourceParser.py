import pytest

from src.trivia.misc.triviaSourceParser import TriviaSourceParser
from src.trivia.misc.triviaSourceParserInterface import TriviaSourceParserInterface
from src.trivia.questions.triviaSource import TriviaSource


class TestTriviaSourceParser:

    parser: TriviaSourceParserInterface = TriviaSourceParser()

    @pytest.mark.asyncio
    async def test_parse_withBongo(self):
        result = await self.parser.parse('bongo')
        assert result is TriviaSource.BONGO

    @pytest.mark.asyncio
    async def test_parse_withEmptyString(self):
        result: TriviaSource | None = None

        with pytest.raises(TypeError):
            result = await self.parser.parse('')

        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withFuntoon(self):
        result = await self.parser.parse('funtoon')
        assert result is TriviaSource.FUNTOON

    @pytest.mark.asyncio
    async def test_parse_withGlacial(self):
        result = await self.parser.parse('glacial')
        assert result is TriviaSource.GLACIAL

    @pytest.mark.asyncio
    async def test_parse_withJService(self):
        result = await self.parser.parse('j_service')
        assert result is TriviaSource.J_SERVICE

    @pytest.mark.asyncio
    async def test_parse_withLordOfTheRings(self):
        result = await self.parser.parse('lord_of_the_rings')
        assert result is TriviaSource.LORD_OF_THE_RINGS

    @pytest.mark.asyncio
    async def test_parse_withMillionaire(self):
        result = await self.parser.parse('millionaire')
        assert result is TriviaSource.MILLIONAIRE

    @pytest.mark.asyncio
    async def test_parse_withNone(self):
        result: TriviaSource | None = None

        with pytest.raises(TypeError):
            result = await self.parser.parse(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_parse_withOpenTrivia(self):
        result = await self.parser.parse('open_trivia')
        assert result is TriviaSource.OPEN_TRIVIA_DATABASE

    @pytest.mark.asyncio
    async def test_parse_withOpenTriviaDatabase(self):
        result = await self.parser.parse('open_trivia_database')
        assert result is TriviaSource.OPEN_TRIVIA_DATABASE

    @pytest.mark.asyncio
    async def test_parse_withOpenTriviaQa(self):
        result = await self.parser.parse('open_trivia_qa')
        assert result is TriviaSource.OPEN_TRIVIA_QA

    @pytest.mark.asyncio
    async def test_parse_withPokeApi(self):
        result = await self.parser.parse('poke_api')
        assert result is TriviaSource.POKE_API

    @pytest.mark.asyncio
    async def test_parse_withQuizApi(self):
        result = await self.parser.parse('quiz_api')
        assert result is TriviaSource.QUIZ_API

    @pytest.mark.asyncio
    async def test_parse_withTheQuestionCo(self):
        result = await self.parser.parse('the_question_co')
        assert result is TriviaSource.THE_QUESTION_CO

    @pytest.mark.asyncio
    async def test_parse_withTriviaDatabase(self):
        result = await self.parser.parse('trivia_database')
        assert result is TriviaSource.TRIVIA_DATABASE

    @pytest.mark.asyncio
    async def test_parse_withWillFryTrivia(self):
        result = await self.parser.parse('will_fry_trivia')
        assert result is TriviaSource.WILL_FRY_TRIVIA

    @pytest.mark.asyncio
    async def test_parse_withWillFryTriviaApi(self):
        result = await self.parser.parse('will_fry_trivia_api')
        assert result is TriviaSource.WILL_FRY_TRIVIA

    @pytest.mark.asyncio
    async def test_parse_withWwtbam(self):
        result = await self.parser.parse('wwtbam')
        assert result is TriviaSource.WWTBAM

    @pytest.mark.asyncio
    async def test_parse_withWhitespaceString(self):
        result: TriviaSource | None = None

        with pytest.raises(TypeError):
            result = await self.parser.parse(' ')

        assert result is None
