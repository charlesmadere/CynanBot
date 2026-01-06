from typing import Final

import pytest

from src.trivia.misc.triviaSourceParser import TriviaSourceParser
from src.trivia.misc.triviaSourceParserInterface import TriviaSourceParserInterface
from src.trivia.questions.triviaSource import TriviaSource


class TestTriviaSourceParser:

    parser: Final[TriviaSourceParserInterface] = TriviaSourceParser()

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

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, TriviaSourceParser)
        assert isinstance(self.parser, TriviaSourceParserInterface)

    @pytest.mark.asyncio
    async def test_serialize(self):
        results: set[str] = set()

        for triviaSource in TriviaSource:
            result = await self.parser.serialize(triviaSource)
            results.add(result)

        assert len(results) == len(TriviaSource)

    @pytest.mark.asyncio
    async def test_serialize_withBongo(self):
        result = await self.parser.serialize(TriviaSource.BONGO)
        assert result == 'bongo'

    @pytest.mark.asyncio
    async def test_serialize_withFuntoon(self):
        result = await self.parser.serialize(TriviaSource.FUNTOON)
        assert result == 'funtoon'

    @pytest.mark.asyncio
    async def test_serialize_withGlacial(self):
        result = await self.parser.serialize(TriviaSource.GLACIAL)
        assert result == 'glacial'

    @pytest.mark.asyncio
    async def test_serialize_withJService(self):
        result = await self.parser.serialize(TriviaSource.J_SERVICE)
        assert result == 'j_service'

    @pytest.mark.asyncio
    async def test_serialize_withLordOfTheRings(self):
        result = await self.parser.serialize(TriviaSource.LORD_OF_THE_RINGS)
        assert result == 'lord_of_the_rings'

    @pytest.mark.asyncio
    async def test_serialize_withMillionaire(self):
        result = await self.parser.serialize(TriviaSource.MILLIONAIRE)
        assert result == 'millionaire'

    @pytest.mark.asyncio
    async def test_serialize_withOpenTriviaDatabase(self):
        result = await self.parser.serialize(TriviaSource.OPEN_TRIVIA_DATABASE)
        assert result == 'open_trivia_database'

    @pytest.mark.asyncio
    async def test_serialize_withOpenTriviaQa(self):
        result = await self.parser.serialize(TriviaSource.OPEN_TRIVIA_QA)
        assert result == 'open_trivia_qa'

    @pytest.mark.asyncio
    async def test_serialize_withPokeApi(self):
        result = await self.parser.serialize(TriviaSource.POKE_API)
        assert result == 'poke_api'

    @pytest.mark.asyncio
    async def test_serialize_withQuizApi(self):
        result = await self.parser.serialize(TriviaSource.QUIZ_API)
        assert result == 'quiz_api'

    @pytest.mark.asyncio
    async def test_serialize_withTheQuestionCo(self):
        result = await self.parser.serialize(TriviaSource.THE_QUESTION_CO)
        assert result == 'the_question_co'

    @pytest.mark.asyncio
    async def test_serialize_withTriviaDatabase(self):
        result = await self.parser.serialize(TriviaSource.TRIVIA_DATABASE)
        assert result == 'trivia_database'

    @pytest.mark.asyncio
    async def test_serialize_withWillFryTrivia(self):
        result = await self.parser.serialize(TriviaSource.WILL_FRY_TRIVIA)
        assert result == 'will_fry_trivia'

    @pytest.mark.asyncio
    async def test_serialize_withWwtbam(self):
        result = await self.parser.serialize(TriviaSource.WWTBAM)
        assert result == 'wwtbam'
