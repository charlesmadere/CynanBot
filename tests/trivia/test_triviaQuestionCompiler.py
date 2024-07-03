import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.trivia.compilers.triviaQuestionCompiler import TriviaQuestionCompiler
from src.trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface


class TestTriviaQuestionCompiler():

    timber: TimberInterface = TimberStub()

    triviaQuestionCompiler: TriviaQuestionCompilerInterface = TriviaQuestionCompiler(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_compileCategory_withEmptyString(self):
        category = await self.triviaQuestionCompiler.compileCategory('')
        assert category is not None
        assert category == ''

    @pytest.mark.asyncio
    async def test_compileCategory_withNewLineString(self):
        category = await self.triviaQuestionCompiler.compileCategory('\n')
        assert category is not None
        assert category == ''

    @pytest.mark.asyncio
    async def test_compileCategory_withNone(self):
        category = await self.triviaQuestionCompiler.compileCategory(None)
        assert category is not None
        assert category == ''

    @pytest.mark.asyncio
    async def test_compileCategory_withWhitespaceString(self):
        category = await self.triviaQuestionCompiler.compileCategory(' ')
        assert category is not None
        assert category == ''

    @pytest.mark.asyncio
    async def test_compileQuestion_withEllipsis(self):
        question = await self.triviaQuestionCompiler.compileQuestion('...And Justice for All')
        assert question is not None
        assert question == '…And Justice for All'

    @pytest.mark.asyncio
    async def test_compileQuestion_withEmptyString(self):
        question = await self.triviaQuestionCompiler.compileQuestion('')
        assert question == ''

    @pytest.mark.asyncio
    async def test_compileQuestion_withBbCodeTags(self):
        question = await self.triviaQuestionCompiler.compileQuestion('[b]Scenes from a Memory[/b]')
        assert question is not None
        assert question == 'Scenes from a Memory'

    @pytest.mark.asyncio
    async def test_compileQuestion_withHtmlTags(self):
        question = await self.triviaQuestionCompiler.compileQuestion('<i>The Great Misdirect</i>')
        assert question is not None
        assert question == 'The Great Misdirect'

    @pytest.mark.asyncio
    async def test_compileQuestion_withManyUnderscores(self):
        question = await self.triviaQuestionCompiler.compileQuestion('The _________ river is very long.')
        assert question is not None
        assert question == 'The ___ river is very long.'

    @pytest.mark.asyncio
    async def test_compileQuestion_withNewLineString(self):
        question = await self.triviaQuestionCompiler.compileQuestion('\n')
        assert question is not None
        assert question == ''

    @pytest.mark.asyncio
    async def test_compileQuestion_withNone(self):
        question = await self.triviaQuestionCompiler.compileQuestion(None)
        assert question is not None
        assert question == ''

    @pytest.mark.asyncio
    async def test_compileQuestion_withExtranneousWhiteSpace(self):
        question = await self.triviaQuestionCompiler.compileQuestion('    \nWhat  country    is  Tokyo in? \n')
        assert question is not None
        assert question == 'What country is Tokyo in?'

    @pytest.mark.asyncio
    async def test_compileQuestion_withWhitespaceString(self):
        question = await self.triviaQuestionCompiler.compileQuestion(' ')
        assert question is not None
        assert question == ''

    @pytest.mark.asyncio
    async def test_compileResponse_withEmptyString(self):
        response = await self.triviaQuestionCompiler.compileResponse('')
        assert response is not None
        assert response == ''

    @pytest.mark.asyncio
    async def test_compileResponse_withNewLineString(self):
        response = await self.triviaQuestionCompiler.compileResponse('\n')
        assert response is not None
        assert response == ''

    @pytest.mark.asyncio
    async def test_compileResponse_withNone(self):
        response = await self.triviaQuestionCompiler.compileResponse(None)
        assert response is not None
        assert response == ''

    @pytest.mark.asyncio
    async def test_compileResponse_withTextReplacementString_theUkraine(self):
        response = await self.triviaQuestionCompiler.compileResponse('The Ukraine')
        assert response == 'Ukraine'

    @pytest.mark.asyncio
    async def test_compileResponse_withWhitespaceString(self):
        response = await self.triviaQuestionCompiler.compileResponse(' ')
        assert response is not None
        assert response == ''

    @pytest.mark.asyncio
    async def test_compileResponses_withEmptyList(self):
        responses = await self.triviaQuestionCompiler.compileResponses(list())
        assert responses is not None
        assert len(responses) == 0

    @pytest.mark.asyncio
    async def test_compileResponses_withMixedList(self):
        responses = await self.triviaQuestionCompiler.compileResponses(
            [ '', ' ', 'One', '', 'Two', '\n', 'Three', None ]
        )

        assert responses is not None
        assert len(responses) == 3
        assert 'One' in responses
        assert 'Two' in responses
        assert 'Three' in responses

    @pytest.mark.asyncio
    async def test_compileResponses_withNone(self):
        responses = await self.triviaQuestionCompiler.compileResponses(None)
        assert responses is not None
        assert len(responses) == 0

    def test_sanity(self):
        assert self.triviaQuestionCompiler is not None
        assert isinstance(self.triviaQuestionCompiler, TriviaQuestionCompilerInterface)
