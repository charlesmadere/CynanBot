from typing import Final

import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.trivia.compilers.triviaQuestionCompiler import TriviaQuestionCompiler
from src.trivia.compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface


class TestTriviaQuestionCompiler:

    timber: Final[TimberInterface] = TimberStub()

    compiler: Final[TriviaQuestionCompilerInterface] = TriviaQuestionCompiler(
        timber = timber,
    )

    @pytest.mark.asyncio
    async def test_compileCategory_withEmptyString(self):
        category = await self.compiler.compileCategory('')
        assert category is not None
        assert category == ''

    @pytest.mark.asyncio
    async def test_compileCategory_withNewLineString(self):
        category = await self.compiler.compileCategory('\n')
        assert category is not None
        assert category == ''

    @pytest.mark.asyncio
    async def test_compileCategory_withNone(self):
        category = await self.compiler.compileCategory(None)
        assert category is not None
        assert category == ''

    @pytest.mark.asyncio
    async def test_compileCategory_withWhitespaceString(self):
        category = await self.compiler.compileCategory(' ')
        assert category is not None
        assert category == ''

    @pytest.mark.asyncio
    async def test_compileQuestion_withEllipsis(self):
        question = await self.compiler.compileQuestion('...And Justice for All')
        assert question is not None
        assert question == '…And Justice for All'

    @pytest.mark.asyncio
    async def test_compileQuestion_withEmptyString(self):
        question = await self.compiler.compileQuestion('')
        assert question == ''

    @pytest.mark.asyncio
    async def test_compileQuestion_withBbCodeTags(self):
        question = await self.compiler.compileQuestion('[b]Scenes from a Memory[/b]')
        assert question is not None
        assert question == 'Scenes from a Memory'

    @pytest.mark.asyncio
    async def test_compileQuestion_withHtmlTags(self):
        question = await self.compiler.compileQuestion('<i>The Great Misdirect</i>')
        assert question is not None
        assert question == 'The Great Misdirect'

    @pytest.mark.asyncio
    async def test_compileQuestion_withManyUnderscores(self):
        question = await self.compiler.compileQuestion('The _________ river is very long.')
        assert question is not None
        assert question == 'The ___ river is very long.'

    @pytest.mark.asyncio
    async def test_compileQuestion_withNewLineString(self):
        question = await self.compiler.compileQuestion('\n')
        assert question is not None
        assert question == ''

    @pytest.mark.asyncio
    async def test_compileQuestion_withNone(self):
        question = await self.compiler.compileQuestion(None)
        assert question is not None
        assert question == ''

    @pytest.mark.asyncio
    async def test_compileQuestion_withExtranneousWhiteSpace(self):
        question = await self.compiler.compileQuestion('    \nWhat  country    is  Tokyo in? \n')
        assert question is not None
        assert question == 'What country is Tokyo in?'

    @pytest.mark.asyncio
    async def test_compileQuestion_withWhitespaceString(self):
        question = await self.compiler.compileQuestion(' ')
        assert question is not None
        assert question == ''

    @pytest.mark.asyncio
    async def test_compileResponse_withEmptyString(self):
        response = await self.compiler.compileResponse('')
        assert response is not None
        assert response == ''

    @pytest.mark.asyncio
    async def test_compileResponse_withNewLineString(self):
        response = await self.compiler.compileResponse('\n')
        assert response is not None
        assert response == ''

    @pytest.mark.asyncio
    async def test_compileResponse_withNone(self):
        response = await self.compiler.compileResponse(None)
        assert response is not None
        assert response == ''

    @pytest.mark.asyncio
    async def test_compileResponse_withTextReplacementString_theUkraine(self):
        response = await self.compiler.compileResponse('The Ukraine')
        assert response == 'Ukraine'

    @pytest.mark.asyncio
    async def test_compileResponse_withWhitespaceString(self):
        response = await self.compiler.compileResponse(' ')
        assert response is not None
        assert response == ''

    @pytest.mark.asyncio
    async def test_compileResponses_withEmptyList(self):
        responses = await self.compiler.compileResponses(list())
        assert responses is not None
        assert len(responses) == 0

    @pytest.mark.asyncio
    async def test_compileResponses_withMixedList(self):
        responses = await self.compiler.compileResponses(
            [ '', ' ', 'One', '', 'Two', '\n', 'Three', None ]
        )

        assert responses is not None
        assert len(responses) == 3
        assert 'One' in responses
        assert 'Two' in responses
        assert 'Three' in responses

    @pytest.mark.asyncio
    async def test_compileResponses_withNone(self):
        responses = await self.compiler.compileResponses(None)
        assert responses is not None
        assert len(responses) == 0

    @pytest.mark.asyncio
    async def test_findAllWordsInQuestion_withIdenticalCategoryAndQuestion(self):
        result = await self.compiler.findAllWordsInQuestion(
            category = 'hello world',
            question = 'Hello, World!'
        )

        assert isinstance(result, frozenset)
        assert len(result) == 2
        assert 'hello' in result
        assert 'world' in result

    @pytest.mark.asyncio
    async def test_findAllWordsInQuestion_withNoneCategory(self):
        result = await self.compiler.findAllWordsInQuestion(
            category = None,
            question = 'Hello, World!'
        )

        assert isinstance(result, frozenset)
        assert len(result) == 2
        assert 'hello' in result
        assert 'world' in result

    @pytest.mark.asyncio
    async def test_findAllWordsInQuestion1(self):
        result = await self.compiler.findAllWordsInQuestion(
            category = 'The Dakotas',
            question = 'This state is south of North Dakota.'
        )

        assert isinstance(result, frozenset)
        assert len(result) == 9
        assert 'the' in result
        assert 'dakotas' in result
        assert 'this' in result
        assert 'state' in result
        assert 'is' in result
        assert 'south' in result
        assert 'of' in result
        assert 'north' in result
        assert 'dakota' in result

    @pytest.mark.asyncio
    async def test_findAllWordsInQuestion2(self):
        result = await self.compiler.findAllWordsInQuestion(
            category = 'Hemispheres',
            question = 'Japan is a country in this hemisphere.'
        )

        assert isinstance(result, frozenset)
        assert len(result) == 7
        assert 'hemispheres' in result
        assert 'japan' in result
        assert 'is' in result
        assert 'country' in result
        assert 'in' in result
        assert 'this' in result
        assert 'hemisphere' in result

    @pytest.mark.asyncio
    async def test_findAllWordsInQuestion3(self):
        result = await self.compiler.findAllWordsInQuestion(
            category = 'Movies',
            question = 'This \"golden\" movie from the 90\'s stars James Bond.',
        )

        assert isinstance(result, frozenset)
        assert len(result) == 10
        assert 'movies' in result
        assert 'this' in result
        assert 'golden' in result
        assert 'movie' in result
        assert 'from' in result
        assert 'the' in result
        assert '90' in result # should we filter out numbers? (I think this is OK)
        assert 'stars' in result
        assert 'james' in result
        assert 'bond' in result

    @pytest.mark.asyncio
    async def test_findAllWordsInQuestion4(self):
        result = await self.compiler.findAllWordsInQuestion(
            category = 'Famous Quotes',
            question = 'This \"splitting\" quote was said by Gert Frobe (Goldfinger) to Sean Connery (James Bond).',
        )

        assert isinstance(result, frozenset)
        assert len(result) == 16
        assert 'famous' in result
        assert 'quotes' in result
        assert 'this' in result
        assert 'splitting' in result
        assert 'quote' in result
        assert 'was' in result
        assert 'said' in result # should we filter out numbers?
        assert 'by' in result
        assert 'gert' in result
        assert 'frobe' in result
        assert 'goldfinger' in result
        assert 'to' in result
        assert 'sean' in result
        assert 'connery' in result
        assert 'james' in result
        assert 'bond' in result

    def test_sanity(self):
        assert self.compiler is not None
        assert isinstance(self.compiler, TriviaQuestionCompiler)
        assert isinstance(self.compiler, TriviaQuestionCompilerInterface)
