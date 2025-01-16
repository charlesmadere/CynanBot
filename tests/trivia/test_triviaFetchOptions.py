from src.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from src.trivia.triviaFetchOptions import TriviaFetchOptions


class TestTriviaFetchOptions:

    def test_areQuestionAnswerTriviaQuestionsEnabled_withQuestionAnswerTriviaConditionsAllowed(self):
        options = TriviaFetchOptions(
            twitchChannel = 'smCharles',
            twitchChannelId = 'c',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.ALLOWED
        )

        assert options.areQuestionAnswerTriviaQuestionsEnabled() is True

    def test_areQuestionAnswerTriviaQuestionsEnabled_withQuestionAnswerTriviaConditionsNotAllowed(self):
        options = TriviaFetchOptions(
            twitchChannel = 'imyt',
            twitchChannelId = 'i',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
        )

        assert options.areQuestionAnswerTriviaQuestionsEnabled() is False

    def test_areQuestionAnswerTriviaQuestionsEnabled_withQuestionAnswerTriviaConditionsRequired(self):
        options = TriviaFetchOptions(
            twitchChannel = 'stashiocat',
            twitchChannelId = 's',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.ALLOWED
        )

        assert options.areQuestionAnswerTriviaQuestionsEnabled() is True

    def test_requireQuestionAnswerTriviaQuestion_withQuestionAnswerTriviaConditionsAllowed(self):
        options = TriviaFetchOptions(
            twitchChannel = 'zoasty',
            twitchChannelId = 'z',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.ALLOWED
        )

        assert options.requireQuestionAnswerTriviaQuestion() is False

    def test_requireQuestionAnswerTriviaQuestion_withQuestionAnswerTriviaConditionsNotAllowed(self):
        options = TriviaFetchOptions(
            twitchChannel = 'behemoth87',
            twitchChannelId = 'b',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
        )

        assert options.requireQuestionAnswerTriviaQuestion() is False

    def test_requireQuestionAnswerTriviaQuestion_withQuestionAnswerTriviaConditionsRequired(self):
        options = TriviaFetchOptions(
            twitchChannel = 'Oatsngoats',
            twitchChannelId = 'o',
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )

        assert options.requireQuestionAnswerTriviaQuestion() is True
