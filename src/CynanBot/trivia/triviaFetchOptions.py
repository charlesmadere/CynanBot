from dataclasses import dataclass

from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions


@dataclass(frozen = True)
class TriviaFetchOptions():
    twitchChannel: str
    twitchChannelId: str
    questionAnswerTriviaConditions: QuestionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED

    def areQuestionAnswerTriviaQuestionsEnabled(self) -> bool:
        return self.questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.ALLOWED \
            or self.questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.REQUIRED

    def requireQuestionAnswerTriviaQuestion(self) -> bool:
        return self.questionAnswerTriviaConditions is QuestionAnswerTriviaConditions.REQUIRED
