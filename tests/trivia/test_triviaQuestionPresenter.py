import pytest

from src.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from src.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from src.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from src.trivia.questions.triviaSource import TriviaSource
from src.trivia.questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from src.trivia.triviaDifficulty import TriviaDifficulty
from src.trivia.triviaQuestionPresenter import TriviaQuestionPresenter
from src.trivia.triviaQuestionPresenterInterface import \
    TriviaQuestionPresenterInterface


class TestTriviaQuestionPresenter:

    multipleChoiceQuestion1: AbsTriviaQuestion = MultipleChoiceTriviaQuestion(
        correctAnswers = [ 'Saturn' ],
        multipleChoiceResponses = [ 'Earth', 'Mars', 'Saturn', 'Venus' ],
        category = None,
        categoryId = None,
        question = 'Which of these planets has a ring?',
        triviaId = 'abc123',
        triviaDifficulty = TriviaDifficulty.EASY,
        originalTriviaSource = None,
        triviaSource = TriviaSource.TRIVIA_DATABASE
    )

    questionAnswerQuestion1: AbsTriviaQuestion = QuestionAnswerTriviaQuestion(
        correctAnswers = [ 'Mercury' ],
        cleanedCorrectAnswers = [ 'mercury' ],
        category = None,
        categoryId = None,
        question = 'This planet is the closest to the sun.',
        originalCorrectAnswers = [ 'Mercury' ],
        triviaId = 'abc123',
        triviaDifficulty = TriviaDifficulty.UNKNOWN,
        originalTriviaSource = None,
        triviaSource = TriviaSource.FUNTOON
    )

    trueFalseQuestion1: AbsTriviaQuestion = TrueFalseTriviaQuestion(
        correctAnswer = True,
        category = None,
        categoryId = None,
        question = 'The earth is a globe.',
        triviaId = 'abc123',
        triviaDifficulty = TriviaDifficulty.UNKNOWN,
        originalTriviaSource = None,
        triviaSource = TriviaSource.TRIVIA_DATABASE
    )

    trueFalseQuestion2: AbsTriviaQuestion = TrueFalseTriviaQuestion(
        correctAnswer = False,
        category = None,
        categoryId = None,
        question = 'The earth is flat.',
        triviaId = 'def456',
        triviaDifficulty = TriviaDifficulty.UNKNOWN,
        originalTriviaSource = None,
        triviaSource = TriviaSource.TRIVIA_DATABASE
    )

    presenter: TriviaQuestionPresenterInterface = TriviaQuestionPresenter()

    @pytest.mark.asyncio
    async def test_getCorrectAnswers_withMultipleChoiceQuestion1(self):
        correctAnswers = await self.presenter.getCorrectAnswers(self.multipleChoiceQuestion1)
        assert correctAnswers == 'The correct answer is: [C] Saturn'

    @pytest.mark.asyncio
    async def test_getCorrectAnswers_withQuestionAnswerQuestion1(self):
        correctAnswers = await self.presenter.getCorrectAnswers(self.questionAnswerQuestion1)
        assert correctAnswers == 'The correct answer is: Mercury'

    @pytest.mark.asyncio
    async def test_getCorrectAnswers_withTrueFalseQuestion1(self):
        correctAnswers = await self.presenter.getCorrectAnswers(self.trueFalseQuestion1)
        assert correctAnswers == 'The correct answer is: true'

    @pytest.mark.asyncio
    async def test_getCorrectAnswers_withTrueFalseQuestion2(self):
        correctAnswers = await self.presenter.getCorrectAnswers(self.trueFalseQuestion2)
        assert correctAnswers == 'The correct answer is: false'

    @pytest.mark.asyncio
    async def test_getPrompt_withTrueFalseQuestion1(self):
        prompt = await self.presenter.getPrompt(self.trueFalseQuestion1)
        assert prompt == '— True or false! The earth is a globe.'

    @pytest.mark.asyncio
    async def test_getPrompt_withTrueFalseQuestion2(self):
        prompt = await self.presenter.getPrompt(self.trueFalseQuestion2)
        assert prompt == '— True or false! The earth is flat.'

    @pytest.mark.asyncio
    async def test_getResponses_withTrueFalseQuestion1(self):
        responses = await self.presenter.getResponses(self.trueFalseQuestion1)
        assert isinstance(responses, list)
        assert len(responses) == 2
        assert responses[0] == 'true'
        assert responses[1] == 'false'

    @pytest.mark.asyncio
    async def test_getResponses_withTrueFalseQuestion2(self):
        responses = await self.presenter.getResponses(self.trueFalseQuestion2)
        assert isinstance(responses, list)
        assert len(responses) == 2
        assert responses[0] == 'true'
        assert responses[1] == 'false'
