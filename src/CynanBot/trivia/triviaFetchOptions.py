from dataclasses import dataclass

from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBot.trivia.questions.triviaSource import TriviaSource

@dataclass(frozen = True)
class TriviaFetchOptions():
    twitchChannel: str
    twitchChannelId: str
    requiredTriviaSource: TriviaSource | None = None
    questionAnswerTriviaConditions: QuestionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED

    def areQuestionAnswerTriviaQuestionsEnabled(self) -> bool:
        return self.questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.ALLOWED \
            or self.questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.REQUIRED

    def requireQuestionAnswerTriviaQuestion(self) -> bool:
        return self.questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.REQUIRED
