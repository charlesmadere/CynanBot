from dataclasses import dataclass

from CynanBot.trivia.additionalAnswers.additionalTriviaAnswer import \
    AdditionalTriviaAnswer
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource


@dataclass(frozen = True)
class AdditionalTriviaAnswers():
    answers: list[AdditionalTriviaAnswer]
    triviaId: str
    triviaQuestionType: TriviaQuestionType
    triviaSource: TriviaSource

    @property
    def answerStrings(self) -> list[str]:
        answerStrings: list[str] = list()

        for answer in self.answers:
            answerStrings.append(answer.answer)

        return answerStrings
