import pytest

from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.questions.trueFalseTriviaQuestion import TrueFalseTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaQuestionPresenter import TriviaQuestionPresenter
from CynanBot.trivia.triviaQuestionPresenterInterface import TriviaQuestionPresenterInterface


class TestTriviaQuestionPresenter():

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
    async def test_getCorrectAnswers_withTrueFalseQuestion1(self):
        correctAnswer = await self.presenter.getCorrectAnswers(self.trueFalseQuestion1)
        assert correctAnswer == 'The correct answer is: true'

    @pytest.mark.asyncio
    async def test_getCorrectAnswers_withTrueFalseQuestion2(self):
        correctAnswer = await self.presenter.getCorrectAnswers(self.trueFalseQuestion2)
        assert correctAnswer == 'The correct answer is: false'

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
