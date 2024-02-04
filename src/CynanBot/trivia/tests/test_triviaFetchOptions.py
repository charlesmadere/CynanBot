from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions


class TestTriviaFetchOptions():

    def test_areQuestionAnswerTriviaQuestionsEnabled_withQuestionAnswerTriviaConditionsAllowed(self):
        options = TriviaFetchOptions(
            twitchChannel = 'smCharles',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.ALLOWED
        )

        assert options.areQuestionAnswerTriviaQuestionsEnabled() is True

    def test_areQuestionAnswerTriviaQuestionsEnabled_withQuestionAnswerTriviaConditionsNotAllowed(self):
        options = TriviaFetchOptions(
            twitchChannel = 'imyt',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
        )

        assert options.areQuestionAnswerTriviaQuestionsEnabled() is False

    def test_areQuestionAnswerTriviaQuestionsEnabled_withQuestionAnswerTriviaConditionsRequired(self):
        options = TriviaFetchOptions(
            twitchChannel = 'stashiocat',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.ALLOWED
        )

        assert options.areQuestionAnswerTriviaQuestionsEnabled() is True

    def test_requireQuestionAnswerTriviaQuestion_withQuestionAnswerTriviaConditionsAllowed(self):
        options = TriviaFetchOptions(
            twitchChannel = 'zoasty',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.ALLOWED
        )

        assert options.requireQuestionAnswerTriviaQuestion() is False

    def test_requireQuestionAnswerTriviaQuestion_withQuestionAnswerTriviaConditionsNotAllowed(self):
        options = TriviaFetchOptions(
            twitchChannel = 'behemoth87',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
        )

        assert options.requireQuestionAnswerTriviaQuestion() is False

    def test_requireQuestionAnswerTriviaQuestion_withQuestionAnswerTriviaConditionsRequired(self):
        options = TriviaFetchOptions(
            twitchChannel = 'Oatsngoats',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )

        assert options.requireQuestionAnswerTriviaQuestion() is True
